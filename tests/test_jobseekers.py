from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

client = TestClient(app)


def setup_module(module):
    # Reset DB before running these tests
    init_db()


def test_create_and_read_jobseeker():
    response = client.post("/jobseekers/", json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"

    # Get one
    resp = client.get(f"/jobseekers/{data['id']}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "John Doe"

    # Get all
    resp2 = client.get("/jobseekers/")
    assert resp2.status_code == 200
    assert any(js["id"] == data["id"] for js in resp2.json())


def test_update_jobseeker_put():
    # Create
    response = client.post("/jobseekers/", json={"name": "Bob", "email": "bob@example.com"})
    jobseeker = response.json()

    # Full replace
    update_resp = client.put(f"/jobseekers/{jobseeker['id']}", json={"name": "Bobby", "email": "bobby@example.com"})
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["name"] == "Bobby"
    assert updated["email"] == "bobby@example.com"


def test_patch_jobseeker():
    # Create
    response = client.post("/jobseekers/", json={"name": "Alice", "email": "alice@example.com"})
    jobseeker = response.json()

    # Patch
    patch_resp = client.patch(f"/jobseekers/{jobseeker['id']}", json={"name": "Alice Updated"})
    assert patch_resp.status_code == 200
    updated = patch_resp.json()
    assert updated["name"] == "Alice Updated"
    assert updated["email"] == "alice@example.com"  # unchanged


def test_delete_jobseeker():
    # Create
    response = client.post("/jobseekers/", json={"name": "Delete Me", "email": "deleteme@example.com"})
    jobseeker = response.json()

    # Delete
    del_resp = client.delete(f"/jobseekers/{jobseeker['id']}")
    assert del_resp.status_code == 200
    assert del_resp.json()["message"] == "JobSeeker deleted successfully"

    # Verify it’s gone
    get_resp = client.get(f"/jobseekers/{jobseeker['id']}")
    assert get_resp.status_code == 404

def test_put_jobseeker():
    # Create JobSeeker
    create_resp = client.post("/jobseekers/", json={"name": "Bob", "email": "bob@example.com"})
    assert create_resp.status_code == 200
    jobseeker = create_resp.json()

    # Full update (PUT)
    put_resp = client.put(f"/jobseekers/{jobseeker['id']}", json={
        "name": "Bob Updated",
        "email": "bob_updated@example.com"
    })
    assert put_resp.status_code == 200
    updated = put_resp.json()

    assert updated["name"] == "Bob Updated"
    assert updated["email"] == "bob_updated@example.com"

    # Verify persisted
    get_resp = client.get(f"/jobseekers/{jobseeker['id']}")
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched == updated
