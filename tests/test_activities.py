import pytest


def test_get_activities(client):
    """Test GET /activities returns all activities"""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Verify the response contains expected activities
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities
    
    # Verify activity structure
    chess_club = activities["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_signup_for_activity(client):
    """Test POST /activities/{activity_name}/signup successfully registers a student"""
    activity_name = "Chess Club"
    email = "alice@mergington.edu"
    
    # Get initial participants count
    response = client.get("/activities")
    initial_participants = response.json()[activity_name]["participants"]
    initial_count = len(initial_participants)
    
    # Sign up the student
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    
    # Verify the participant was added
    response = client.get("/activities")
    updated_participants = response.json()[activity_name]["participants"]
    assert len(updated_participants) == initial_count + 1
    assert email in updated_participants


def test_unregister_from_activity(client):
    """Test DELETE /activities/{activity_name}/unregister successfully removes a participant"""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants
    
    # Verify the participant exists
    response = client.get("/activities")
    participants = response.json()[activity_name]["participants"]
    initial_count = len(participants)
    assert email in participants
    
    # Unregister the student
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    
    # Verify the participant was removed
    response = client.get("/activities")
    updated_participants = response.json()[activity_name]["participants"]
    assert len(updated_participants) == initial_count - 1
    assert email not in updated_participants
