from typing import Optional
from datetime import datetime
from pydantic import validator

from src.interfaces.schemas.base import BaseSchema


class IncomeSchema(BaseSchema):
    amount: float
    description: str = ""
    release_date: Optional[datetime] = None

    @validator('release_date', pre=True)
    def parse_release_date(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, '%Y-%m-%d')
        return v
