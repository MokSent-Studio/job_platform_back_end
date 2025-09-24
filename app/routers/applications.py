from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

router = APIRouter()


# --- Create Application ---
@router.post("/", response_model=schemas.ApplicationRead)
def create_application_put(application: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    return crud.create_application(db=db, application=application)


# --- Read All Applications ---
@router.get("/", response_model=List[schemas.ApplicationRead])
def read_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_applications(db, skip=skip, limit=limit)


# --- Read Single Application ---
@router.get("/{application_id}", response_model=schemas.ApplicationRead)
def read_application(application_id: int, db: Session = Depends(get_db)):
    db_application = crud.get_application(db, application_id=application_id)
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_application


# --- Delete Application ---
class Message(schemas.BaseModel):
    message: str


@router.delete("/{application_id}", response_model=Message)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    db_application = crud.get_application(db, application_id=application_id)
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(db_application)
    db.commit()
    return {"message": "Application deleted successfully"}

# --- Update Application ---
@router.patch("/{application_id}", response_model=schemas.ApplicationRead)
def update_application(application_id: int, application: schemas.ApplicationUpdate, db: Session = Depends(get_db)):
    db_app = crud.update_application_patch(db, application_id, application)
    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_app

@router.put("/{application_id}", response_model=schemas.ApplicationRead)
def update_application_put(application_id: int, application: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    db_application = crud.update_application_put(db, application_id=application_id, application=application)
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_application
