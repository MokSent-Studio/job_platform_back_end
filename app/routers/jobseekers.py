from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

router = APIRouter()


# --- Create JobSeeker ---
@router.post("/", response_model=schemas.JobSeekerRead)
def create_jobseeker_put(jobseeker: schemas.JobSeekerCreate, db: Session = Depends(get_db)):
    return crud.create_jobseeker(db=db, jobseeker=jobseeker)


# --- Read All JobSeekers ---
@router.get("/", response_model=List[schemas.JobSeekerRead])
def read_jobseekers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_jobseekers(db, skip=skip, limit=limit)


# --- Read Single JobSeeker ---
@router.get("/{jobseeker_id}", response_model=schemas.JobSeekerRead)
def read_jobseeker(jobseeker_id: int, db: Session = Depends(get_db)):
    db_jobseeker = crud.get_jobseeker(db, jobseeker_id=jobseeker_id)
    if not db_jobseeker:
        raise HTTPException(status_code=404, detail="JobSeeker not found")
    return db_jobseeker


# --- Delete JobSeeker ---
class Message(schemas.BaseModel):
    message: str


@router.delete("/{jobseeker_id}", response_model=Message)
def delete_jobseeker(jobseeker_id: int, db: Session = Depends(get_db)):
    db_jobseeker = crud.get_jobseeker(db, jobseeker_id=jobseeker_id)
    if not db_jobseeker:
        raise HTTPException(status_code=404, detail="JobSeeker not found")

    db.delete(db_jobseeker)
    db.commit()
    return {"message": "JobSeeker deleted successfully"}

# --- Update JobSeeker ---
@router.patch("/{jobseeker_id}", response_model=schemas.JobSeekerRead)
def update_jobseeker(jobseeker_id: int, jobseeker: schemas.JobSeekerUpdate, db: Session = Depends(get_db)):
    db_jobseeker = crud.update_jobseeker_patch(db, jobseeker_id, jobseeker)
    if not db_jobseeker:
        raise HTTPException(status_code=404, detail="JobSeeker not found")
    return db_jobseeker

# --- Full Update JobSeeker (PUT) ---
@router.put("/{jobseeker_id}", response_model=schemas.JobSeekerRead)
def update_jobseeker_put(jobseeker_id: int, jobseeker: schemas.JobSeekerCreate, db: Session = Depends(get_db)):
    db_jobseeker = crud.update_jobseeker_put(db, jobseeker_id, jobseeker)
    if not db_jobseeker:
        raise HTTPException(status_code=404, detail="JobSeeker not found")
    return db_jobseeker