from datetime import date, timedelta
from typing import List
from sqlalchemy.orm import Session
import models

def get_overtime_risk_nurses(db: Session, max_hours: int = 40) -> List[models.Nurse]:
    """
    CDSS Rule 1: Overtime and Burnout Risk
    Filters nurses whose weekly working hours exceed the specified threshold (default: 40 hours)
    and present a risk of overtime/burnout.
    """
    return db.query(models.Nurse).filter(models.Nurse.weekly_hours > max_hours).all()


def get_nurses_eligible_for_shift(db: Session, min_rest_days: int = 1) -> List[models.Nurse]:
    """
    CDSS Rule 2: Mandatory Rest Period Control
    Retrieves nurses who have completed the required rest period (default: 1 day) 
    since their last shift and are eligible for scheduling.
    """
    today = date.today()
    max_last_shift_date = today - timedelta(days=min_rest_days)
    
    return db.query(models.Nurse).filter(models.Nurse.last_shift_date <= max_last_shift_date).all()


def evaluate_nurse_burnout_score(nurse: models.Nurse) -> dict:
    """
    CDSS Rule 3: Clinical Risk Assessment
    Generates a dynamic burnout risk score and clinical recommendation 
    based on weekly working hours and experience.
    """
    risk_level = "LOW"
    recommendation = "Eligible for shift assignment."

    if nurse.weekly_hours >= 48:
        risk_level = "HIGH"
        recommendation = "Critical overtime risk! Immediate rest period required."
    elif nurse.weekly_hours > 40:
        risk_level = "MEDIUM"
        recommendation = "Moderate overtime risk. Consider reducing shift hours."

    return {
        "nurse_id": nurse.id,
        "name": nurse.name,
        "weekly_hours": nurse.weekly_hours,
        "risk_level": risk_level,
        "recommendation": recommendation
    }