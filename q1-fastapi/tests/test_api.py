import pytest
from fastapi.testclient import TestClient

import sys
from pathlib import Path

# Add q1-fastapi directory to sys.path so 'app' is always cleanly resolvable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app
from app.storage import clear_storage

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_in_memory_storage():
    """Ensure in-memory storage is reset before and after every test."""
    clear_storage()
    yield
    clear_storage()


def test_create_credit_transaction_success():
    payload = {
        "user_id": "U1001",
        "amount": 1500,
        "type": "credit",
        "timestamp": "2026-09-18T10:30:00",
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == "U1001"
    assert data["amount"] == 1500.0
    assert data["type"] == "credit"
    assert data["timestamp"] == "2026-09-18T10:30:00"


def test_create_debit_transaction_success():
    payload = {
        "user_id": "U1001",
        "amount": 500,
        "type": "debit",
        "timestamp": "2026-09-18T11:00:00",
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == "U1001"
    assert data["amount"] == 500.0
    assert data["type"] == "debit"
    assert data["timestamp"] == "2026-09-18T11:00:00"


def test_get_transactions_for_user():
    # Insert two transactions for user U1001
    t1 = {
        "user_id": "U1001",
        "amount": 1000,
        "type": "credit",
        "timestamp": "2026-09-18T10:00:00",
    }
    t2 = {
        "user_id": "U1001",
        "amount": 250,
        "type": "debit",
        "timestamp": "2026-09-18T12:00:00",
    }
    client.post("/transactions", json=t1)
    client.post("/transactions", json=t2)

    response = client.get("/transactions/U1001")
    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) == 2
    assert transactions[0]["amount"] == 1000.0
    assert transactions[0]["type"] == "credit"
    assert transactions[1]["amount"] == 250.0
    assert transactions[1]["type"] == "debit"


def test_transactions_belonging_to_another_user_are_not_returned():
    user1_tx = {
        "user_id": "USER_A",
        "amount": 100,
        "type": "credit",
        "timestamp": "2026-09-18T10:00:00",
    }
    user2_tx = {
        "user_id": "USER_B",
        "amount": 200,
        "type": "credit",
        "timestamp": "2026-09-18T10:05:00",
    }
    client.post("/transactions", json=user1_tx)
    client.post("/transactions", json=user2_tx)

    resp_a = client.get("/transactions/USER_A")
    assert resp_a.status_code == 200
    records_a = resp_a.json()
    assert len(records_a) == 1
    assert records_a[0]["user_id"] == "USER_A"
    assert records_a[0]["amount"] == 100.0

    resp_b = client.get("/transactions/USER_B")
    assert resp_b.status_code == 200
    records_b = resp_b.json()
    assert len(records_b) == 1
    assert records_b[0]["user_id"] == "USER_B"
    assert records_b[0]["amount"] == 200.0


def test_user_summary_calculation():
    # As per prompt sample: total_credit: 5000, total_debit: 2500, balance: 2500
    txs = [
        {"user_id": "U1001", "amount": 3000, "type": "credit", "timestamp": "2026-09-18T09:00:00"},
        {"user_id": "U1001", "amount": 2000, "type": "credit", "timestamp": "2026-09-18T10:00:00"},
        {"user_id": "U1001", "amount": 2500, "type": "debit", "timestamp": "2026-09-18T11:00:00"},
    ]
    for tx in txs:
        client.post("/transactions", json=tx)

    response = client.get("/transactions/U1001/summary")
    assert response.status_code == 200
    summary = response.json()
    assert summary["total_credit"] == 5000.0
    assert summary["total_debit"] == 2500.0
    assert summary["balance"] == 2500.0


def test_empty_user_summary():
    response = client.get("/transactions/NON_EXISTENT_USER/summary")
    assert response.status_code == 200
    summary = response.json()
    assert summary["total_credit"] == 0.0
    assert summary["total_debit"] == 0.0
    assert summary["balance"] == 0.0


def test_empty_user_transactions():
    response = client.get("/transactions/NON_EXISTENT_USER")
    assert response.status_code == 200
    assert response.json() == []


def test_reject_negative_amount():
    payload = {
        "user_id": "U1001",
        "amount": -500,
        "type": "credit",
        "timestamp": "2026-09-18T10:00:00",
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 422


def test_reject_zero_amount():
    payload = {
        "user_id": "U1001",
        "amount": 0,
        "type": "credit",
        "timestamp": "2026-09-18T10:00:00",
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 422


def test_reject_invalid_transaction_type():
    payload = {
        "user_id": "U1001",
        "amount": 100,
        "type": "transfer",
        "timestamp": "2026-09-18T10:00:00",
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 422


def test_reject_invalid_timestamp():
    payload = {
        "user_id": "U1001",
        "amount": 100,
        "type": "credit",
        "timestamp": "not-a-valid-datetime",
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 422


@pytest.mark.parametrize("missing_field", ["user_id", "amount", "type", "timestamp"])
def test_reject_missing_required_fields(missing_field):
    payload = {
        "user_id": "U1001",
        "amount": 100,
        "type": "credit",
        "timestamp": "2026-09-18T10:00:00",
    }
    del payload[missing_field]
    response = client.post("/transactions", json=payload)
    assert response.status_code == 422


def test_reject_empty_user_id_in_payload():
    payload_empty = {
        "user_id": "",
        "amount": 100,
        "type": "credit",
        "timestamp": "2026-09-18T10:00:00",
    }
    response = client.post("/transactions", json=payload_empty)
    assert response.status_code == 422

    payload_whitespace = {
        "user_id": "   ",
        "amount": 100,
        "type": "credit",
        "timestamp": "2026-09-18T10:00:00",
    }
    response = client.post("/transactions", json=payload_whitespace)
    assert response.status_code == 422


def test_reject_whitespace_user_id_in_path():
    # Whitespace in path param should return 400
    response = client.get("/transactions/%20")
    assert response.status_code == 400

    response_summary = client.get("/transactions/%20/summary")
    assert response_summary.status_code == 400


def test_summary_floating_point_precision():
    txs = [
        {"user_id": "PRECISION_USER", "amount": 19.99, "type": "credit", "timestamp": "2026-09-18T10:00:00"},
        {"user_id": "PRECISION_USER", "amount": 10.01, "type": "credit", "timestamp": "2026-09-18T10:05:00"},
        {"user_id": "PRECISION_USER", "amount": 5.50, "type": "debit", "timestamp": "2026-09-18T10:10:00"},
    ]
    for tx in txs:
        client.post("/transactions", json=tx)

    response = client.get("/transactions/PRECISION_USER/summary")
    assert response.status_code == 200
    summary = response.json()
    assert summary["total_credit"] == 30.00
    assert summary["total_debit"] == 5.50
    assert summary["balance"] == 24.50
