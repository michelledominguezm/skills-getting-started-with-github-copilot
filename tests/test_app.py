import copy

import pytest
from fastapi.testclient import TestClient
from src.app import activities, app

client = TestClient(app)

@pytest.fixture(autouse=True)
def restore_activities():
    original_activities = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original_activities))


def test_get_activities_returns_expected_structure():
    # Arrange
    expected_keys = {"Chess Club", "Programming Class", "Gym Class"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert expected_keys.issubset(set(data))
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert data["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Chess Club"
    new_email = "teststudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={new_email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_email} for {activity_name}"}
    assert new_email in activities[activity_name]["participants"]


def test_remove_participant_unregisters_existing_student():
    # Arrange
    activity_name = "Programming Class"
    email_to_remove = "emma@mergington.edu"
    assert email_to_remove in activities[activity_name]["participants"]

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email_to_remove}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email_to_remove} from {activity_name}"}
    assert email_to_remove not in activities[activity_name]["participants"]


def test_remove_participant_returns_404_for_missing_email():
    # Arrange
    activity_name = "Programming Class"
    missing_email = "missing@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={missing_email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
