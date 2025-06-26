from pydantic import BaseModel
from typing import Optional

class RecordBase(BaseModel):
    title: str
    description: Optional[str] = None

class RecordCreate(RecordBase):
    pass

class RecordUpdate(RecordBase):
    done: Optional[bool] = False

class RecordInDB(RecordBase):
    id: int
    done: bool

    class Config:
        orm_mode = True
