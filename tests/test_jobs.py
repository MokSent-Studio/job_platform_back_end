from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_and_read_job():
    # First create a company to attach the job to
    company_resp = client.post("/companies/", json={"name": "JobCo", "website": "http://jobco.com"})
    assert company_resp.status_code == 200
    company_id = company_resp.json()["id"]

    # Create job
    job_resp = client.post(
        "/jobs/",
        json={"title": "Developer", "description": "Build stuff", "salary": 60000, "company_id": company_id},
    )
    assert job_resp.status_code == 200
    job_data = job_resp.json()
    assert job_data["title"] == "Developer"
    job_id = job_data["id"]

    # Read job
    read_resp = client.get(f"/jobs/{job_id}")
    assert read_resp.status_code == 200
    assert read_resp.json()["title"] == "Developer"

    # Read all jobs
    list_resp = client.get("/jobs/")
    assert list_resp.status_code == 200
    assert any(j["title"] == "Developer" for j in list_resp.json())


def test_update_job():
    # Company
    company_resp = client.post("/companies/", json={"name": "UpdateCo", "website": "http://updateco.com"})
    company_id = company_resp.json()["id"]

    # Create job
    job_resp = client.post(
        "/jobs/",
        json={"title": "Tester", "description": "Test things", "salary": 40000, "company_id": company_id},
    )
    job_id = job_resp.json()["id"]

    # Update job
    update_resp = client.put(
        f"/jobs/{job_id}",
        json={"title": "QA Engineer", "description": "Ensure quality", "salary": 50000, "company_id": company_id},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "QA Engineer"


def test_delete_job():
    # Company
    company_resp = client.post("/companies/", json={"name": "DeleteCo", "website": "http://deleteco.com"})
    company_id = company_resp.json()["id"]

    # Create job
    job_resp = client.post(
        "/jobs/",
        json={"title": "Intern", "description": "Learn", "salary": 0, "company_id": company_id},
    )
    job_id = job_resp.json()["id"]

    # Delete job
    del_resp = client.delete(f"/jobs/{job_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["message"] == "Job deleted successfully"

    # Verify it's gone
    get_resp = client.get(f"/jobs/{job_id}")
    assert get_resp.status_code == 404

def test_patch_job(client):
    # Create company first
    company_response = client.post("/companies/", json={"name": "PatchCo"})
    company_id = company_response.json()["id"]

    # Create job
    job_response = client.post("/jobs/", json={"title": "Dev", "description": "Old desc", "company_id": company_id})
    job = job_response.json()

    # Patch job
    patch_response = client.patch(f"/jobs/{job['id']}", json={"description": "New desc"})
    assert patch_response.status_code == 200
    updated = patch_response.json()
    assert updated["description"] == "New desc"
    assert updated["title"] == "Dev"  # unchanged

def test_put_job():
    # Create a company first
    company = client.post("/companies/", json={"name": "JobCo", "website": "http://jobco.com"}).json()

    # Create job
    job = client.post("/jobs/", json={
        "title": "Old Job",
        "description": "Old desc",
        "salary": 1000,
        "company_id": company["id"]
    }).json()

    # Full update
    put_resp = client.put(f"/jobs/{job['id']}", json={
        "title": "New Job",
        "description": "New description",
        "salary": 2000,
        "company_id": company["id"]
    })
    assert put_resp.status_code == 200
    updated = put_resp.json()

    assert updated["title"] == "New Job"
    assert updated["description"] == "New description"
    assert updated["salary"] == 2000

