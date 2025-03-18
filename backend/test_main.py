import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import models
import database
from main import app, get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
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

@pytest.fixture
def setup_database():
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after tests
    models.Base.metadata.drop_all(bind=engine)

def test_signup_success(setup_database):
    response = client.post(
        "/api/signup",
        json={
            "email": "test@example.com",
            "password": "password123",
            "username": "testuser"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data

def test_signup_duplicate_email(setup_database):
    # First signup
    client.post(
        "/api/signup",
        json={
            "email": "test@example.com",
            "password": "password123",
            "username": "testuser"
        }
    )
    # Second signup with same email
    response = client.post(
        "/api/signup",
        json={
            "email": "test@example.com",
            "password": "password123",
            "username": "testuser2"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_signup_invalid_data(setup_database):
    response = client.post(
        "/api/signup",
        json={
            "email": "invalid-email",
            "password": "",
            "username": "testuser"
        }
    )
    assert response.status_code == 422

def test_login_success(setup_database):
    # First create a user
    client.post(
        "/api/signup",
        json={
            "email": "test@example.com",
            "password": "password123",
            "username": "testuser"
        }
    )
    # Try to login
    response = client.post(
        "/api/login",
        data={
            "username": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(setup_database):
    # First create a user
    client.post(
        "/api/signup",
        json={
            "email": "test@example.com",
            "password": "password123",
            "username": "testuser"
        }
    )
    # Try to login with wrong password
    response = client.post(
        "/api/login",
        data={
            "username": "test@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_login_nonexistent_user(setup_database):
    response = client.post(
        "/api/login",
        data={
            "username": "nonexistent@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_get_current_user(setup_database):
    # First create a user and login
    client.post(
        "/api/signup",
        json={
            "email": "test@example.com",
            "password": "password123",
            "username": "testuser"
        }
    )
    login_response = client.post(
        "/api/login",
        data={
            "username": "test@example.com",
            "password": "password123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Try to get current user
    response = client.get(
        "/api/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"

def test_get_current_user_invalid_token(setup_database):
    response = client.get(
        "/api/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials" 