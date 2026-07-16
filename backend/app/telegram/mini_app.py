"""Telegram Mini App — авторизация и конфигурация."""

import hashlib
import hmac
import json
import time
from urllib.parse import unquote
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.database.session import get_db
from app.repositories.user_repo import UserRepository

router = APIRouter(prefix="/telegram", tags=["Telegram"])


class TelegramInitData(BaseModel):
    """Данные инициализации Telegram Mini App."""
    query_id: Optional[str] = None
    user: Optional[dict] = None
    auth_date: int
    hash: str


class TelegramUser(BaseModel):
    """Пользователь Telegram."""
    id: int
    is_bot: bool = False
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None


class TelegramAuthResponse(BaseModel):
    """Ответ авторизации."""
    access_token: str
    user_id: str
    is_new_user: bool


def verify_telegram_data(init_data: str) -> dict:
    """
    Верификация данных Telegram Mini App.
    https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    """
    try:
        # Parse init data
        data_check_string = []
        data = {}
        
        for item in init_data.split("&"):
            key, value = item.split("=", 1)
            if key == "hash":
                continue
            data[key] = value
            data_check_string.append(f"{key}={value}")
        
        # Sort and join
        data_check_string.sort()
        data_check_string = "\n".join(data_check_string)
        
        # Create secret key
        secret_key = hmac.new(
            settings.TELEGRAM_BOT_TOKEN.encode(),
            msg=b"WebAppData",
            digestmod=hashlib.sha256,
        ).digest()
        
        # Calculate hash
        calculated_hash = hmac.new(
            secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()
        
        # Verify hash
        if calculated_hash != data.get("hash"):
            raise HTTPException(status_code=401, detail="Invalid Telegram data")
        
        # Check auth_date (max 24 hours old)
        auth_date = int(data.get("auth_date", 0))
        if time.time() - auth_date > 86400:
            raise HTTPException(status_code=401, detail="Auth data expired")
        
        return data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid init data: {str(e)}")


@router.post("/auth", response_model=TelegramAuthResponse)
async def telegram_auth(
    init_data: TelegramInitData,
    db: AsyncSession = Depends(get_db),
):
    """
    Авторизация через Telegram Mini App.
    Верифицирует данные и создаёт/находит пользователя.
    """
    # For development, skip verification
    if settings.DEBUG:
        user_data = init_data.user or {}
    else:
        # Verify Telegram data
        if init_data.query_id:
            verified_data = verify_telegram_data(
                f"query_id={init_data.query_id}&"
                f"user={json.dumps(init_data.user)}&"
                f"auth_date={init_data.auth_date}&"
                f"hash={init_data.hash}"
            )
            user_data = json.loads(verified_data.get("user", "{}"))
        else:
            user_data = init_data.user or {}
    
    # Extract user info
    telegram_id = user_data.get("id")
    if not telegram_id:
        raise HTTPException(status_code=400, detail="Invalid user data")
    
    # Get or create user
    user_repo = UserRepository(db)
    user = await user_repo.get_by_telegram_id(telegram_id)
    
    is_new = False
    if not user:
        is_new = True
        user = await user_repo.get_or_create_by_telegram(
            telegram_id=telegram_id,
            username=user_data.get("username"),
            language_code=user_data.get("language_code", "en"),
        )
    
    # Generate token (simplified - use JWT in production)
    from datetime import datetime, timedelta
    import jwt
    
    token_payload = {
        "user_id": str(user.id),
        "telegram_id": telegram_id,
        "exp": datetime.utcnow() + timedelta(days=7),
    }
    access_token = jwt.encode(
        token_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    
    return TelegramAuthResponse(
        access_token=access_token,
        user_id=str(user.id),
        is_new_user=is_new,
    )


@router.get("/config")
async def get_telegram_config():
    """Получить конфигурацию для Telegram Mini App."""
    return {
        "bot_username": settings.TELEGRAM_BOT_TOKEN.split(":")[0] if settings.TELEGRAM_BOT_TOKEN else None,
        "mini_app_url": settings.TELEGRAM_MINI_APP_URL,
    }
