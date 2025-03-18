import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app, get_db
import models

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after tests
    Base.metadata.drop_all(bind=engine)

def test_signup_success():
    response = client.post(
        "/api/signup",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "username": "testuser"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data
    assert "password" not in data

def test_signup_duplicate_email():
    # First signup
    client.post(
        "/api/signup",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "username": "testuser"
        }
    )
    # Second signup with same email
    response = client.post(
        "/api/signup",
        json={
            "email": "test@example.com",
            "password": "testpassword2",
            "username": "testuser2"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_signup_invalid_data():
    response = client.post(
        "/api/signup",
        json={
            "email": "invalid-email",
            "password": "",  # Empty password
            "username": "testuser"
        }
    )
    assert response.status_code == 422  # Validation error 