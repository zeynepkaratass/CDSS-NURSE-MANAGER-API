from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CDSS-NURSE-MANAGER API",
    description="API for Nurse Shift Systems in Hospitals",
    version="1.0.0"
)


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the CDSS-NURSE-MANAGER API! Visit /docs for full API documentation."}

@app.get("/nurses/", response_model=List[schemas.NurseResponse], tags=["Nurses"])
def get_all_nurses(db: Session = Depends(get_db)):
    """Retrieve all nurses."""
    return db.query(models.Nurse).all()

@app.get("/nurses/{nurse_id}", response_model=schemas.NurseResponse, tags=["Nurses"])
def get_nurse_by_id(nurse_id: int, db: Session = Depends(get_db)):
    """Retrieve a single nurse by ID."""
    nurse = db.query(models.Nurse).filter(models.Nurse.id == nurse_id).first()
    if not nurse:
        raise HTTPException(status_code=404, detail="Nurse not found.")
    return nurse


@app.post("/nurses/", response_model=schemas.NurseResponse, status_code=status.HTTP_201_CREATED, tags=["Nurses"])
def create_nurse(nurse: schemas.NurseCreate, db: Session = Depends(get_db)):
    """Create a new nurse record."""
    db_nurse = models.Nurse(**nurse.model_dump())  # Pydantic verisini SQLAlchemy modeline çevirir
    db.add(db_nurse)
    db.commit()
    db.refresh(db_nurse)
    return db_nurse

@app.put("/nurses/{nurse_id}", response_model=schemas.NurseResponse, tags=["Nurses"])
def update_nurse(nurse_id: int, nurse_data: schemas.NurseCreate, db: Session = Depends(get_db)):
    """Update an existing nurse's details."""
    db_nurse = db.query(models.Nurse).filter(models.Nurse.id == nurse_id).first()
    if not db_nurse:
        raise HTTPException(status_code=404, detail="Nurse not found.")
    
    for key, value in nurse_data.model_dump().items():
        setattr(db_nurse, key, value)
        
    db.commit()
    db.refresh(db_nurse)
    return db_nurse

@app.delete("/nurses/{nurse_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Nurses"])
def delete_nurse(nurse_id: int, db: Session = Depends(get_db)):
    """Delete a nurse record."""
    db_nurse = db.query(models.Nurse).filter(models.Nurse.id == nurse_id).first()
    if not db_nurse:
        raise HTTPException(status_code=404, detail="Nurse not found.")
    
    db.delete(db_nurse)
    db.commit()
    return None

