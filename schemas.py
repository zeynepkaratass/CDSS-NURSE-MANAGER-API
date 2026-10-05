from pydantic import BaseModel
from datetime import date
from typing import Optional

# 1. Base Schema
class NurseBase(BaseModel):
    name: str
    department: Optional[str] = None
    education_level: str
    experience_years: Optional[int] = None
    weekly_hours: Optional[int] = None
    last_shift_date: date

# 2. Schema for creating a nurse
class NurseCreate(NurseBase):
    pass

# 3. Schema for returning a nurse
class NurseResponse(NurseBase):
    id: int

    class Config:
        from_attributes = True
        