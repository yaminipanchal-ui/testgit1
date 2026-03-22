def test_get_activities(client):
    # Arrange
    # (client fixture provides app instance)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert payload == {"message": f"Signed up {email} for {activity_name}"}

    # Act (verify state)
    get_response = client.get("/activities")

    # Assert (verify state)
    assert email in get_response.json()[activity_name]["participants"]


def test_signup_for_activity_already_signed_up(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_activity_not_found(client):
    # Arrange
    bad_activity_name = "Unknown Club"

    # Act
    response = client.post(f"/activities/{bad_activity_name}/signup", params={"email": "test@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_for_activity_full_capacity(client):
    # Arrange
    activity_name = "Tennis Club"

    # Act: fill to capacity first
    for i in range(8):
        email = f"player{i}@mergington.edu"
        resp = client.post(f"/activities/{activity_name}/signup", params={"email": email})
        assert resp.status_code == 200

    full_email = "overflow@mergington.edu"

    # Act: attempt one more
    response = client.post(f"/activities/{activity_name}/signup", params={"email": full_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_unregister_participant_success(client):
    # Arrange
    activity_name = "Gym Class"
    participant = "john@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{participant}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {participant} from {activity_name}"

    # Act (verify state)
    get_response = client.get("/activities")

    # Assert
    assert participant not in get_response.json()[activity_name]["participants"]


def test_unregister_participant_not_found(client):
    # Arrange
    activity_name = "Gym Class"
    participant = "doesnotexist@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{participant}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_activity_not_found(client):
    # Arrange
    missing_activity = "Unknown Club"

    # Act
    response = client.delete(f"/activities/{missing_activity}/participants/foo@bar.com")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
