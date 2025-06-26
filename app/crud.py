from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from . import models, schemas

async def create_entry(db: AsyncSession, entry: schemas.EntryCreate) -> models.Entry:
    db_entry = models.Entry(**entry.dict())
    db.add(db_entry)
    await db.commit()
    await db.refresh(db_entry)
    return db_entry

async def get_entry(db: AsyncSession, entry_id: int) -> Optional[models.Entry]:
    result = await db.execute(select(models.Entry).where(models.Entry.id == entry_id))
    return result.scalars().first()

async def get_entries(db: AsyncSession) -> List[models.Entry]:
    result = await db.execute(select(models.Entry))
    return result.scalars().all()

async def update_entry(db: AsyncSession, entry_id: int, entry_update: schemas.EntryUpdate) -> Optional[models.Entry]:
    result = await db.execute(select(models.Entry).where(models.Entry.id == entry_id))
    db_entry = result.scalars().first()
    if not db_entry:
        return None
    update_data = entry_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_entry, key, value)
    await db.commit()
    await db.refresh(db_entry)
    return db_entry

async def delete_entry(db: AsyncSession, entry_id: int) -> bool:
    result = await db.execute(select(models.Entry).where(models.Entry.id == entry_id))
    db_entry = result.scalars().first()
    if not db_entry:
        return False
    await db.execute(delete(models.Entry).where(models.Entry.id == entry_id))
    await db.commit()
    return True

async def mark_as_done(db: AsyncSession, entry_id: int) -> Optional[models.Entry]:
    result = await db.execute(select(models.Entry).where(models.Entry.id == entry_id))
    db_entry = result.scalars().first()
    if not db_entry:
        return None
    db_entry.is_done = True
    await db.commit()
    await db.refresh(db_entry)
    return db_entry
