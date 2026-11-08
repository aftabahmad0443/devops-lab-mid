import pytest
from app import app, submissions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Clear database before each test
        submissions.clear()
        yield client

# Test Case 1: Complete details & valid submission URL
def test_valid_submission(client):
    payload = {
        "name": "Ali Khan",
        "reg_number": "FA21-BCS-001",
        "title": "DevOps Assignment 1",
        "submission_url": "https://github.com/user/devops-lab"
    }
    response = client.post('/submit', json=payload)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["status"] == "success"
    
    # Verify it appears in submission list
    list_response = client.get('/submissions')
    assert list_response.status_code == 200
    assert len(list_response.get_json()["submissions"]) == 1

# Test Case 2: Missing registration number
def test_missing_registration_number(client):
    payload = {
        "name": "Ali Khan",
        "reg_number": "",  # Missing
        "title": "DevOps Assignment 1",
        "submission_url": "https://github.com/user/devops-lab"
    }
    response = client.post('/submit', json=payload)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["status"] == "error"
    assert "required" in json_data["message"]

# Test Case 3: Invalid submission URL
def test_invalid_submission_url(client):
    payload = {
        "name": "Ali Khan",
        "reg_number": "FA21-BCS-001",
        "title": "DevOps Assignment 1",
        "submission_url": "invalid-url-string"  # Invalid
    }
    response = client.post('/submit', json=payload)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["status"] == "error"
    assert "Invalid submission URL" in json_data["message"]