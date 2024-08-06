import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


@pytest.fixture
def valid_address():
    return "0x6105f0b07341eE41562fd359Ff705a8698Dd3109"


@pytest.fixture
def invalid_address():
    return "invalid_address"


@pytest.fixture
def chain_id():
    return "1"


def test_get_wallet_assets_valid_address(valid_address, chain_id):
    response = client.get(f"/wallet/{valid_address}/assets?chain_id={chain_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_wallet_assets_invalid_address(invalid_address, chain_id):
    response = client.get(f"/wallet/{invalid_address}/assets?chain_id={chain_id}")
    assert response.status_code == 400


def test_get_wallet_total_value_valid_address(valid_address, chain_id):
    response = client.get(f"/wallet/{valid_address}/total_value?chain_id={chain_id}")
    assert response.status_code == 200
    assert "total_value_usd" in response.json()


def test_get_wallet_total_value_invalid_address(invalid_address, chain_id):
    response = client.get(f"/wallet/{invalid_address}/total_value?chain_id={chain_id}")
    assert response.status_code == 400


def test_get_wallet_transactions_valid_address(valid_address, chain_id):
    page = 0
    page_size = 10
    response = client.get(f"/wallet/{valid_address}/transactions?chain_id={chain_id}&page={page}&page_size={page_size}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


if __name__ == "__main__":
    pytest.main()
