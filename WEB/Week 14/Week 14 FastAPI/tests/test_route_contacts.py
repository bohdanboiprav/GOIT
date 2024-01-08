from unittest.mock import Mock, patch, AsyncMock

import pytest

from src.services.auth import auth_service


def test_get_contacts(client, get_token):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 0


def test_get_contacts_by(client, get_token):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        name = "John"
        surname = "Doe"
        email = "john.doe@example.com"
        response = client.get("api/contacts/by?name={name}&surname={surname}&email={email}", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 0


def test_get_birthdays(client, get_token):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts/birthdays", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 0


def test_get_contact(client, get_token):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts/1", headers=headers)
        assert response.status_code == 404, response.text
        data = response.json()
        assert len(data) == 1


def test_create_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("api/contacts/create", headers=headers, json={
            "name": "string",
            "surname": "string",
            "email": "user@example.com",
            "phone": "string",
            "date_of_birth": "2004-01-08",
            "additional_info": "string"
        })
        assert response.status_code == 200, response.text
        data = response.json()
        assert "id" in data
        assert data["name"] == "string"
        assert data["email"] == "user@example.com"


def test_populate_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("api/contacts/populate/2", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert "Contacts populated" in data


def test_update_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.put("api/contacts/1", headers=headers, json={
            "name": "string",
            "surname": "string",
            "email": "user@example.com",
            "phone": "string",
            "date_of_birth": "2004-01-08",
            "additional_info": "string"
        })
        assert response.status_code == 200, response.text
        data = response.json()
        assert "id" in data
        assert data["name"] == "string"
        assert data["email"] == "user@example.com"


def test_remove_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.delete("api/contacts/1", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert "id" in data
