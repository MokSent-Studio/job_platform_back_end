from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

client = TestClient(app)


def setup_module(module):
    # Reset DB for clean state
    init_db()


def create_base_entities():
    """Helper to create company, job, jobseeker for application tests"""
    company = client.post("/companies/", json={"name": "AppTestCo", "website": "https://apptest.com"}).json()
    job = client.post("/jobs/", json={
        "title": "QA Tester",
        "description": "Test the platform",
        "salary": 4000,
        "company_id": company["id"]
    }).json()
    jobseeker = client.post("/jobseekers/", json={"name": "Alice", "email": "alice@example.com"}).json()
    return company, job, jobseeker


def test_create_and_read_application():
    company, job, jobseeker = create_base_entities()

    # Create an application
    response = client.post("/applications/", json={
        "cover_letter": "I am very motivated",
        "job_id": job["id"],
        "jobseeker_id": jobseeker["id"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["job"]["id"] == job["id"]
    assert data["jobseeker"]["id"] == jobseeker["id"]
    app_id = data["id"]

    # Fetch single application
    get_one = client.get(f"/applications/{app_id}")
    assert get_one.status_code == 200
    assert get_one.json()["id"] == app_id

    # Fetch all applications
    get_all = client.get("/applications/")
    assert get_all.status_code == 200
    assert any(app["id"] == app_id for app in get_all.json())


def test_update_application_put():
    company, job, jobseeker = create_base_entities()

    # Create application
    app_data = client.post("/applications/", json={
        "cover_letter": "Old Letter",
        "job_id": job["id"],
        "jobseeker_id": jobseeker["id"]
    }).json()
    app_id = app_data["id"]

    # Full replace (PUT)
    update_resp = client.put(f"/applications/{app_id}", json={
        "cover_letter": "New Full Letter",
        "job_id": job["id"],
        "jobseeker_id": jobseeker["id"]
    })
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["cover_letter"] == "New Full Letter"


def test_update_application_patch():
    company, job, jobseeker = create_base_entities()

    # Create application
    app_data = client.post("/applications/", json={
        "cover_letter": "Patch Old",
        "job_id": job["id"],
        "jobseeker_id": jobseeker["id"]
    }).json()
    app_id = app_data["id"]

    # Partial update (PATCH)
    patch_resp = client.patch(f"/applications/{app_id}", json={"cover_letter": "Patch Updated"})
    assert patch_resp.status_code == 200
    patched = patch_resp.json()
    assert patched["cover_letter"] == "Patch Updated"


def test_delete_application():
    company, job, jobseeker = create_base_entities()

    # Create application
    app_data = client.post("/applications/", json={
        "cover_letter": "Delete me",
        "job_id": job["id"],
        "jobseeker_id": jobseeker["id"]
    }).json()
    app_id = app_data["id"]

    # Delete application
    del_resp = client.delete(f"/applications/{app_id}")
    assert del_resp.status_code == 200

    # Verify it no longer exists
    get_resp = client.get(f"/applications/{app_id}")
    assert get_resp.status_code == 404
