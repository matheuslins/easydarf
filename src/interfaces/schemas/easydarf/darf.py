from src.interfaces.schemas.base import BaseSchema
from pydantic import validator


class DarfSchema(BaseSchema):
    month: int

    @validator('month')
    def month_must_be_valid(cls, value):
        if 0 < value <= 12:
            return value
        raise ValueError('Month must be an integer between [1-12]')
