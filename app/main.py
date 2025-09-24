from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import companies, jobs, jobseekers, applications
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    init_db()  # create tables
    print("✅ Database initialized")
    yield
    # --- Shutdown ---
    print("👋 Shutting down app...")

app = FastAPI(title="Job Platform MVP", version="v1", lifespan=lifespan)


# Routers
app.include_router(companies.router, prefix="/companies", tags=["companies"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(jobseekers.router, prefix="/jobseekers", tags=["jobseekers"])
app.include_router(applications.router, prefix="/applications", tags=["applications"])
