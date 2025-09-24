from sqlalchemy.orm import Session
from app import models, schemas

# --- Company ---
def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(**company.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()

def get_companies(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Company).offset(skip).limit(limit).all()

def update_company_put(db: Session, company_id: int, company: schemas.CompanyCreate):
    """Full update (PUT) — replaces all fields"""
    db_company = get_company(db, company_id)
    if not db_company:
        return None
    for key, value in company.model_dump().items():
        setattr(db_company, key, value)
    db.commit()
    db.refresh(db_company)
    return db_company

def update_company_patch(db: Session, company_id: int, company: schemas.CompanyUpdate):
    """Partial update (PATCH) — updates only provided fields"""
    db_company = get_company(db, company_id)
    if not db_company:
        return None
    for key, value in company.model_dump(exclude_unset=True).items():
        setattr(db_company, key, value)
    db.commit()
    db.refresh(db_company)
    return db_company

def delete_company(db: Session, company_id: int):
    db_company = get_company(db, company_id)
    if not db_company:
        return None
    db.delete(db_company)
    db.commit()
    return db_company


# --- Job ---
def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def get_jobs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Job).offset(skip).limit(limit).all()

def update_job_put(db: Session, job_id: int, job: schemas.JobCreate):
    db_job = get_job(db, job_id)
    if not db_job:
        return None
    for key, value in job.model_dump().items():
        setattr(db_job, key, value)
    db.commit()
    db.refresh(db_job)
    return db_job

def update_job_patch(db: Session, job_id: int, job: schemas.JobUpdate):
    db_job = get_job(db, job_id)
    if not db_job:
        return None
    for key, value in job.model_dump(exclude_unset=True).items():
        setattr(db_job, key, value)
    db.commit()
    db.refresh(db_job)
    return db_job

def delete_job(db: Session, job_id: int):
    db_job = get_job(db, job_id)
    if not db_job:
        return None
    db.delete(db_job)
    db.commit()
    return db_job

# --- Application ---
def create_application(db: Session, application: schemas.ApplicationCreate):
    db_app = models.Application(**application.model_dump())
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

def get_application(db: Session, application_id: int):
    return db.query(models.Application).filter(models.Application.id == application_id).first()

def get_applications(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Application).offset(skip).limit(limit).all()

def update_application_put(db: Session, application_id: int, application: schemas.ApplicationCreate):
    db_app = get_application(db, application_id)
    if not db_app:
        return None
    for key, value in application.model_dump().items():
        setattr(db_app, key, value)
    db.commit()
    db.refresh(db_app)
    return db_app

def update_application_patch(db: Session, application_id: int, application: schemas.ApplicationUpdate):
    db_app = get_application(db, application_id)
    if not db_app:
        return None
    for key, value in application.model_dump(exclude_unset=True).items():
        setattr(db_app, key, value)
    db.commit()
    db.refresh(db_app)
    return db_app

def delete_application(db: Session, application_id: int):
    db_app = get_application(db, application_id)
    if not db_app:
        return None
    db.delete(db_app)
    db.commit()
    return db_app

# --- JobSeeker ---
from sqlalchemy.orm import Session
from app import models, schemas

def create_jobseeker(db: Session, jobseeker: schemas.JobSeekerCreate):
    db_jobseeker = models.JobSeeker(**jobseeker.model_dump())
    db.add(db_jobseeker)
    db.commit()
    db.refresh(db_jobseeker)
    return db_jobseeker

def get_jobseeker(db: Session, jobseeker_id: int):
    return db.query(models.JobSeeker).filter(models.JobSeeker.id == jobseeker_id).first()

def get_jobseekers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.JobSeeker).offset(skip).limit(limit).all()

def update_jobseeker_put(db: Session, jobseeker_id: int, jobseeker: schemas.JobSeekerCreate):
    db_jobseeker = get_jobseeker(db, jobseeker_id)
    if not db_jobseeker:
        return None
    for key, value in jobseeker.model_dump().items():
        setattr(db_jobseeker, key, value)
    db.commit()
    db.refresh(db_jobseeker)
    return db_jobseeker

def update_jobseeker_patch(db: Session, jobseeker_id: int, jobseeker: schemas.JobSeekerUpdate):
    db_jobseeker = get_jobseeker(db, jobseeker_id)
    if not db_jobseeker:
        return None
    for key, value in jobseeker.model_dump(exclude_unset=True).items():
        setattr(db_jobseeker, key, value)
    db.commit()
    db.refresh(db_jobseeker)
    return db_jobseeker

def delete_jobseeker(db: Session, jobseeker_id: int):
    db_jobseeker = get_jobseeker(db, jobseeker_id)
    if not db_jobseeker:
        return None
    db.delete(db_jobseeker)
    db.commit()
    return db_jobseeker