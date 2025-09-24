from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    website = Column(String, nullable=True)

    jobs = relationship("Job", back_populates="company")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    salary = Column(Float, nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job")

class JobSeeker(Base):
    __tablename__ = "jobseekers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    applications = relationship("Application", back_populates="jobseeker")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    cover_letter = Column(Text, nullable=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    jobseeker_id = Column(Integer, ForeignKey("jobseekers.id"))

    job = relationship("Job", back_populates="applications")
    jobseeker = relationship("JobSeeker", back_populates="applications")
