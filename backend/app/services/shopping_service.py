"""Shopping Service — умные покупки."""

import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.shopping import ShoppingList, ShoppingItem


class ShoppingService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_list(
        self,
        user_id: uuid.UUID,
        name: str,
        budget: float | None = None,
    ) -> ShoppingList:
        shopping_list = ShoppingList(
            user_id=user_id,
            name=name,
            budget=budget,
        )
        self.db.add(shopping_list)
        await self.db.flush()
        return shopping_list

    async def add_item(
        self,
        list_id: uuid.UUID,
        name: str,
        quantity: int = 1,
        estimated_price: float | None = None,
        category: str | None = None,
    ) -> ShoppingItem:
        item = ShoppingItem(
            list_id=list_id,
            name=name,
            quantity=quantity,
            estimated_price=estimated_price,
            category=category,
        )
        self.db.add(item)
        await self.db.flush()
        return item

    async def get_lists(self, user_id: uuid.UUID) -> list[ShoppingList]:
        query = (
            select(ShoppingList)
            .where(ShoppingList.user_id == user_id)
            .where(ShoppingList.is_completed == False)
            .order_by(ShoppingList.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_list_items(self, list_id: uuid.UUID) -> list[ShoppingItem]:
        query = (
            select(ShoppingItem)
            .where(ShoppingItem.list_id == list_id)
            .order_by(ShoppingItem.is_purchased, ShoppingItem.created_at)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def mark_purchased(self, item_id: uuid.UUID, actual_price: float | None = None) -> ShoppingItem | None:
        query = select(ShoppingItem).where(ShoppingItem.id == item_id)
        result = await self.db.execute(query)
        item = result.scalar_one_or_none()
        
        if item:
            item.is_purchased = True
            if actual_price:
                item.actual_price = actual_price
            await self.db.flush()
        
        return item

    async def get_total(self, list_id: uuid.UUID) -> dict:
        items = await self.get_list_items(list_id)
        
        total_estimated = sum(
            (item.estimated_price or 0) * item.quantity
            for item in items
        )
        total_actual = sum(
            (item.actual_price or 0) * item.quantity
            for item in items if item.is_purchased
        )
        
        return {
            "estimated": total_estimated,
            "actual": total_actual,
            "remaining": total_estimated - total_actual,
            "items_count": len(items),
            "purchased_count": sum(1 for i in items if i.is_purchased),
        }
