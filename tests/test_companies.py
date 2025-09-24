from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_and_read_company():
    # Create
    response = client.post("/companies/", json={"name": "Acme Corp", "website": "https://acme.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Acme Corp"
    company_id = data["id"]

    # Read one
    resp2 = client.get(f"/companies/{company_id}")
    assert resp2.status_code == 200
    assert resp2.json()["name"] == "Acme Corp"

    # Read all
    resp3 = client.get("/companies/")
    assert resp3.status_code == 200
    assert any(c["name"] == "Acme Corp" for c in resp3.json())


def test_update_company():
    # Create a company first
    response = client.post("/companies/", json={"name": "Test Co", "website": "http://test.com"})
    assert response.status_code == 200
    company_id = response.json()["id"]

    # Update it
    update_resp = client.put(
        f"/companies/{company_id}",
        json={"name": "Updated Co", "website": "http://updated.com"}
    )
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["name"] == "Updated Co"
    assert updated["website"] == "http://updated.com"


def test_delete_company():
    # Create a company first
    response = client.post("/companies/", json={"name": "Delete Me", "website": "http://deleteme.com"})
    assert response.status_code == 200
    company_id = response.json()["id"]

    # Delete it
    del_resp = client.delete(f"/companies/{company_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["message"] == "Company deleted successfully"

    # Verify it's gone
    get_resp = client.get(f"/companies/{company_id}")
    assert get_resp.status_code == 404


def test_patch_company():
    # Create company
    response = client.post("/companies/", json={"name": "OldCo", "website": "http://old.com"})
    assert response.status_code == 200
    company = response.json()

    # Patch company
    patch_response = client.patch(f"/companies/{company['id']}", json={"website": "http://new.com"})
    assert patch_response.status_code == 200
    updated = patch_response.json()
    assert updated["website"] == "http://new.com"
    assert updated["name"] == "OldCo"  # unchanged
