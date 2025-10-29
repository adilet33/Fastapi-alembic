from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional


class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: str
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class TaskCreate(BaseModel):
    title: str
    description: str



class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None



class TaskDelete(BaseModel):
    id: UUID


    