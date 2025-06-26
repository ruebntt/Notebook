from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import List
import models
import schemas
import crud

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/daily_planner"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

app = FastAPI()

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@app.on_event("startup")
async def startup():
    # Создать таблицы
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.get("/records/", response_model=List[schemas.RecordInDB])
async def read_records(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)):
    records = await crud.get_records(session, skip=skip, limit=limit)
    return records

@app.get("/records/{record_id}", response_model=schemas.RecordInDB)
async def read_record(record_id: int, session: AsyncSession = Depends(get_session)):
    record = await crud.get_record(session, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@app.post("/records/", response_model=schemas.RecordInDB)
async def create_record(record: schemas.RecordCreate, session: AsyncSession = Depends(get_session)):
    return await crud.create_record(session, record)

@app.put("/records/{record_id}", response_model=schemas.RecordInDB)
async def update_record(record_id: int, record: schemas.RecordUpdate, session: AsyncSession = Depends(get_session)):
    db_record = await crud.get_record(session, record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    return await crud.update_record(session, db_record, record)

@app.delete("/records/{record_id}")
async def delete_record(record_id: int, session: AsyncSession = Depends(get_session)):
    db_record = await crud.get_record(session, record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    await crud.delete_record(session, db_record)
    return {"detail": "Record deleted"}

@app.patch("/records/{record_id}/done", response_model=schemas.RecordInDB)
async def mark_done(record_id: int, done: bool, session: AsyncSession = Depends(get_session)):
    db_record = await crud.get_record(session, record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    return await crud.set_done(session, db_record, done)
