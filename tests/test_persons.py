import json
import pytest
from app import create_app
from app.db import db
from app.models import Person

@pytest.fixture
def client(tmp_path, monkeypatch):
    # use sqlite in-memory for unit tests
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client

def test_create_and_get_person(client):
    payload = {"name":"John Doe","age":30,"address":"Somewhere","work":"Eng"}
    r = client.post('/api/v1/persons', json=payload)
    assert r.status_code == 201
    assert 'Location' in r.headers
    # extract id
    loc = r.headers['Location']
    pid = int(loc.rstrip('/').split('/')[-1])

    r2 = client.get(f'/api/v1/persons/{pid}')
    assert r2.status_code == 200
    body = r2.get_json()
    assert body['id'] == pid
    assert body['name'] == payload['name']

def test_get_all_persons(client):
    # create two
    client.post('/api/v1/persons', json={"name":"A"})
    client.post('/api/v1/persons', json={"name":"B"})
    r = client.get('/api/v1/persons')
    assert r.status_code == 200
    arr = r.get_json()
    assert isinstance(arr, list)
    assert len(arr) >= 2

def test_patch_person(client):
    r = client.post('/api/v1/persons', json={"name":"PatchMe","address":"Old"})
    pid = int(r.headers['Location'].split('/')[-1])
    r2 = client.patch(f'/api/v1/persons/{pid}', json={"name":"NewName","address":"New"})
    assert r2.status_code == 200
    body = r2.get_json()
    assert body['name'] == "NewName"
    assert body['address'] == "New"

def test_delete_person(client):
    r = client.post('/api/v1/persons', json={"name":"ToDelete"})
    pid = int(r.headers['Location'].split('/')[-1])
    r2 = client.delete(f'/api/v1/persons/{pid}')
    assert r2.status_code == 204
    r3 = client.get(f'/api/v1/persons/{pid}')
    assert r3.status_code == 404