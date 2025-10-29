import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("description" in v and "participants" in v for v in data.values())

def test_signup_and_unregister():
    # Use a test email and activity
    test_email = "pytest-student@mergington.edu"
    activity_name = next(iter(client.get("/activities").json().keys()))

    # Sign up
    signup_url = f"/activities/{activity_name}/signup?email={test_email}"
    response = client.post(signup_url)
    assert response.status_code == 200
    assert "message" in response.json()

    # Check participant is added
    activities = client.get("/activities").json()
    assert test_email in activities[activity_name]["participants"]

    # Unregister
    unregister_url = f"/activities/{activity_name}/unregister?email={test_email}"
    response = client.post(unregister_url)
    assert response.status_code == 200
    assert "message" in response.json()

    # Check participant is removed
    activities = client.get("/activities").json()
    assert test_email not in activities[activity_name]["participants"]
