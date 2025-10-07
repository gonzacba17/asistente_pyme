from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    hashed_password: str

class Comprobante(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    ocr_text: Optional[str] = None
    due_date: Optional[date] = None
    uploaded_by_id: Optional[int] = Field(default=None, foreign_key="user.id")
