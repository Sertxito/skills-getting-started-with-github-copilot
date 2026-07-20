"""
Tests for the Mergington High School Activities API
Following the AAA (Arrange-Act-Assert) pattern.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


class TestGetActivities:
    """Tests for the GET /activities endpoint"""

    def test_get_all_activities(self, client):
        """Test retrieving all activities"""
        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_activity_has_required_fields(self, client):
        """Test that each activity has required fields"""
        # Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_participants_are_list_of_emails(self, client):
        """Test that participants are stored as email addresses"""
        # Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        chess_club = data.get("Chess Club")
        assert chess_club is not None
        assert len(chess_club["participants"]) > 0
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]


class TestSignupForActivity:
    """Tests for the POST /activities/{activity_name}/signup endpoint"""

    def test_signup_new_participant(self, client):
        """Test signing up a new participant for an activity"""
        # Arrange
        email = "newemail@mergington.edu"
        activity = "Basketball Team"

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_signup_participant_appears_in_list(self, client):
        """Test that signed-up participant appears in the activity list"""
        # Arrange
        email = "testuser@mergington.edu"
        activity = "Soccer Club"

        # Act
        client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        response = client.get("/activities")
        data = response.json()
        assert email in data[activity]["participants"]

    def test_signup_nonexistent_activity(self, client):
        """Test signing up for a non-existent activity"""
        # Arrange
        email = "test@mergington.edu"
        activity = "Nonexistent Activity"

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_duplicate_email(self, client):
        """Test that duplicate signups are rejected"""
        # Arrange
        email = "duplicate@mergington.edu"
        activity = "Drama Club"
        client.post(f"/activities/{activity}/signup?email={email}")

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()

    def test_signup_at_capacity(self, client):
        """Test that signup fails when activity is at capacity"""
        # Arrange
        activity = "Basketball Team"
        current_data = client.get("/activities").json()
        current_count = len(current_data[activity]["participants"])
        max_participants = current_data[activity]["max_participants"]
        for i in range(max_participants - current_count):
            client.post(f"/activities/{activity}/signup?email=capacity{i}@mergington.edu")

        # Act
        response = client.post(f"/activities/{activity}/signup?email=overflow@mergington.edu")

        # Assert
        assert response.status_code == 400
        assert "capacity" in response.json()["detail"].lower()

    def test_signup_empty_email(self, client):
        """Test signup with empty email"""
        # Arrange
        activity = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity}/signup?email=")

        # Assert
        assert response.status_code in [200, 422]


class TestUnregisterFromActivity:
    """Tests for the DELETE /activities/{activity_name}/signup endpoint"""

    def test_unregister_participant(self, client):
        """Test unregistering a participant from an activity"""
        # Arrange
        email = "unregister@mergington.edu"
        activity = "Art Studio"
        client.post(f"/activities/{activity}/signup?email={email}")

        # Act
        response = client.delete(f"/activities/{activity}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        assert email in response.json()["message"]

    def test_unregister_participant_removed_from_list(self, client):
        """Test that unregistered participant is removed from the activity"""
        # Arrange
        email = "removeme@mergington.edu"
        activity = "Debate Team"
        client.post(f"/activities/{activity}/signup?email={email}")

        # Act
        client.delete(f"/activities/{activity}/signup?email={email}")

        # Assert
        response = client.get("/activities")
        assert email not in response.json()[activity]["participants"]

    def test_unregister_nonexistent_activity(self, client):
        """Test unregistering from a non-existent activity"""
        # Arrange
        email = "test@mergington.edu"
        activity = "Fake Activity"

        # Act
        response = client.delete(f"/activities/{activity}/signup?email={email}")

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_unregister_not_registered(self, client):
        """Test unregistering someone who isn't registered"""
        # Arrange
        email = "notregistered@mergington.edu"
        activity = "Science Club"

        # Act
        response = client.delete(f"/activities/{activity}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"].lower()


class TestRootEndpoint:
    """Tests for the GET / endpoint"""

    def test_root_redirects_to_index(self, client):
        """Test that root endpoint redirects to static/index.html"""
        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]


class TestActivityCapacity:
    """Tests for activity capacity management"""

    def test_max_participants_respected(self, client):
        """Test that participant count never exceeds max_participants"""
        # Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        for activity_name, activity_data in data.items():
            assert len(activity_data["participants"]) <= activity_data["max_participants"]

    def test_capacity_counter(self, client):
        """Test that signing up increments the participant count"""
        # Arrange
        email = "capacitytest@mergington.edu"
        activity = "Science Club"
        initial_count = len(client.get("/activities").json()[activity]["participants"])

        # Act
        client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        data = client.get("/activities").json()
        assert len(data[activity]["participants"]) == initial_count + 1


class TestDataPersistence:
    """Tests for data persistence during a session"""

    def test_signup_persists_across_requests(self, client):
        """Test that signup data persists in subsequent requests"""
        # Arrange
        email = "persistent@mergington.edu"
        activity = "Programming Class"
        client.post(f"/activities/{activity}/signup?email={email}")

        # Act & Assert (multiple subsequent requests)
        for _ in range(3):
            response = client.get("/activities")
            assert email in response.json()[activity]["participants"]

    def test_multiple_signups_accumulate(self, client):
        """Test that multiple signups accumulate correctly"""
        # Arrange
        activity = "Gym Class"
        initial_count = len(client.get("/activities").json()[activity]["participants"])

        # Act
        for i in range(3):
            client.post(f"/activities/{activity}/signup?email=multi{i}@mergington.edu")

        # Assert
        final_count = len(client.get("/activities").json()[activity]["participants"])
        assert final_count == initial_count + 3



class TestSignupForActivity:
    """Tests for the POST /activities/{activity_name}/signup endpoint"""

    def test_signup_new_participant(self, client):
        """Test signing up a new participant for an activity"""
        response = client.post(
            "/activities/Basketball Team/signup?email=newemail@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "newemail@mergington.edu" in data["message"]
        assert "Basketball Team" in data["message"]

    def test_signup_participant_appears_in_list(self, client):
        """Test that signed-up participant appears in the activity list"""
        test_email = "testuser@mergington.edu"
        
        # Sign up
        client.post(f"/activities/Soccer Club/signup?email={test_email}")
        
        # Verify in list
        response = client.get("/activities")
        data = response.json()
        assert test_email in data["Soccer Club"]["participants"]

    def test_signup_nonexistent_activity(self, client):
        """Test signing up for a non-existent activity"""
        response = client.post(
            "/activities/Nonexistent Activity/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_duplicate_email(self, client):
        """Test that duplicate signups are rejected"""
        email = "duplicate@mergington.edu"
        activity = "Drama Club"
        
        # First signup
        response1 = client.post(f"/activities/{activity}/signup?email={email}")
        assert response1.status_code == 200
        
        # Second signup with same email
        response2 = client.post(f"/activities/{activity}/signup?email={email}")
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"].lower()

    def test_signup_at_capacity(self, client):
        """Test that signup fails when activity is at capacity"""
        activity = "Basketball Team"
        
        # Get current state of the activity
        response = client.get("/activities")
        data = response.json()
        current_participants = len(data[activity]["participants"])
        max_participants = data[activity]["max_participants"]
        spots_available = max_participants - current_participants
        
        # Fill up the remaining spots
        for i in range(spots_available):
            email = f"capacity{i}@mergington.edu"
            response = client.post(f"/activities/{activity}/signup?email={email}")
            assert response.status_code == 200
        
        # Try to sign up one more (should fail)
        response = client.post(
            f"/activities/{activity}/signup?email=overflow@mergington.edu"
        )
        assert response.status_code == 400
        assert "capacity" in response.json()["detail"].lower()

    def test_signup_empty_email(self, client):
        """Test signup with empty email"""
        response = client.post("/activities/Chess Club/signup?email=")
        # Should either fail or accept empty string (depending on validation)
        # This tests the current behavior
        assert response.status_code in [200, 422]


class TestUnregisterFromActivity:
    """Tests for the DELETE /activities/{activity_name}/signup endpoint"""

    def test_unregister_participant(self, client):
        """Test unregistering a participant from an activity"""
        email = "unregister@mergington.edu"
        activity = "Art Studio"
        
        # Sign up first
        client.post(f"/activities/{activity}/signup?email={email}")
        
        # Unregister
        response = client.delete(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
        assert email in response.json()["message"]

    def test_unregister_participant_removed_from_list(self, client):
        """Test that unregistered participant is removed from the activity"""
        email = "removeme@mergington.edu"
        activity = "Debate Team"
        
        # Sign up
        client.post(f"/activities/{activity}/signup?email={email}")
        
        # Verify they're in the list
        response = client.get("/activities")
        assert email in response.json()[activity]["participants"]
        
        # Unregister
        client.delete(f"/activities/{activity}/signup?email={email}")
        
        # Verify they're removed
        response = client.get("/activities")
        assert email not in response.json()[activity]["participants"]

    def test_unregister_nonexistent_activity(self, client):
        """Test unregistering from a non-existent activity"""
        response = client.delete(
            "/activities/Fake Activity/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_unregister_not_registered(self, client):
        """Test unregistering someone who isn't registered"""
        response = client.delete(
            "/activities/Science Club/signup?email=notregistered@mergington.edu"
        )
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"].lower()


class TestRootEndpoint:
    """Tests for the GET / endpoint"""

    def test_root_redirects_to_index(self, client):
        """Test that root endpoint redirects to static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307  # Temporary redirect
        assert "/static/index.html" in response.headers["location"]


class TestActivityCapacity:
    """Tests for activity capacity management"""

    def test_max_participants_respected(self, client):
        """Test that max_participants limit is enforced"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert len(activity_data["participants"]) <= activity_data["max_participants"]

    def test_capacity_counter(self, client):
        """Test that capacity is correctly calculated"""
        # Sign up to an activity
        email = "capacitytest@mergington.edu"
        client.post("/activities/Science Club/signup?email={email}")
        
        # Check the count
        response = client.get("/activities")
        data = response.json()
        
        activity = data["Science Club"]
        assert len(activity["participants"]) <= activity["max_participants"]


class TestDataPersistence:
    """Tests for data persistence during a session"""

    def test_signup_persists_across_requests(self, client):
        """Test that signup data persists in subsequent requests"""
        email = "persistent@mergington.edu"
        activity = "Programming Class"
        
        # Sign up
        client.post(f"/activities/{activity}/signup?email={email}")
        
        # Make multiple requests and verify data persists
        for _ in range(3):
            response = client.get("/activities")
            assert email in response.json()[activity]["participants"]

    def test_multiple_signups_accumulate(self, client):
        """Test that multiple signups accumulate correctly"""
        activity = "Gym Class"
        initial_count = 0
        
        # Get initial count
        response = client.get("/activities")
        initial_count = len(response.json()[activity]["participants"])
        
        # Sign up 3 new people
        for i in range(3):
            client.post(f"/activities/{activity}/signup?email=multi{i}@mergington.edu")
        
        # Verify count increased
        response = client.get("/activities")
        final_count = len(response.json()[activity]["participants"])
        assert final_count == initial_count + 3
