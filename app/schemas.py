from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# --- Company ---
class CompanyBase(BaseModel):
    name: str
    website: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyRead(CompanyBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    website: Optional[str] = None


# --- Job ---
class JobBase(BaseModel):
    title: str
    description: str
    salary: Optional[float] = None

class JobCreate(JobBase):
    company_id: int

class JobRead(JobBase):
    id: int
    company: CompanyRead
    model_config = ConfigDict(from_attributes=True)

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    salary: Optional[float] = None
    company_id: Optional[int] = None


# --- JobSeeker ---
class JobSeekerBase(BaseModel):
    name: str
    email: EmailStr

class JobSeekerCreate(JobSeekerBase):
    pass

class JobSeekerRead(JobSeekerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class JobSeekerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

# --- Application ---
class ApplicationBase(BaseModel):
    cover_letter: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    job_id: int
    jobseeker_id: int

class ApplicationRead(ApplicationBase):
    id: int
    job: JobRead
    jobseeker: JobSeekerRead
    model_config = ConfigDict(from_attributes=True)

class ApplicationUpdate(BaseModel):
    cover_letter: Optional[str] = None
    job_id: Optional[int] = None
    jobseeker_id: Optional[int] = None
