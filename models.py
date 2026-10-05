from sqlalchemy import Column, Integer, String, Date
from database import Base

class Nurse(Base):
    __tablename__ = "list_of_nurses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(String, index=True) 
    education_level = Column(String, nullable=False)
    experience_years = Column(Integer)
    weekly_hours = Column(Integer)
    last_shift_date = Column(Date, nullable=False)
    
    


