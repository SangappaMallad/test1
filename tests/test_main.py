import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.main import app, get_db   # adjust import if file name differs

from app.schemas import ProductCreate


# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create test DB tables
Base.metadata.create_all(bind=engine)


# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# -----------------------
# TEST: CREATE PRODUCT
# -----------------------
def test_create_product():
    response = client.post(
        "/products",
        json={
            "name": "Laptop",
            "price": 50000
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "Laptop"
    assert data["price"] == 50000
    assert "id" in data


# -----------------------
# TEST: GET PRODUCTS
# -----------------------
def test_get_products():
    response = client.get("/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)