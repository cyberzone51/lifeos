"""Auth API — эндпоинты аутентификации."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Auth"])


class TelegramLoginRequest(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo_url: Optional[str] = None
    auth_date: int
    hash: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str


@router.post("/telegram", response_model=TokenResponse)
async def telegram_login(request: TelegramLoginRequest):
    """Вход через Telegram."""
    # TODO: Верификация hash от Telegram
    return TokenResponse(
        access_token="mock-access-token",
        refresh_token="mock-refresh-token",
        user_id="mock-user-id",
    )


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    """Обновить access token."""
    return {"access_token": "new-access-token"}


@router.post("/logout")
async def logout():
    """Выход из системы."""
    return {"status": "logged_out"}
