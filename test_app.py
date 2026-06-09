import pytest
from app import app, db, Task

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

# ── CREATE ───────────────────────────────────────────

def test_create_task_success(client):
    res = client.post('/tasks', json={'title': 'Write unit tests', 'description': 'Cover all endpoints'})
    assert res.status_code == 201
    assert res.get_json()['title'] == 'Write unit tests'

def test_create_task_missing_title(client):
    res = client.post('/tasks', json={'description': 'No title here'})
    assert res.status_code == 400
    assert 'error' in res.get_json()

def test_create_task_invalid_status(client):
    res = client.post('/tasks', json={'title': 'Bad status', 'status': 'flying'})
    assert res.status_code == 400

def test_create_task_default_status(client):
    res = client.post('/tasks', json={'title': 'Default status task'})
    assert res.get_json()['status'] == 'pending'

# ── READ ─────────────────────────────────────────────

def test_get_all_tasks_empty(client):
    res = client.get('/tasks')
    assert res.status_code == 200
    assert res.get_json() == []

def test_get_all_tasks_returns_created(client):
    client.post('/tasks', json={'title': 'Task A'})
    client.post('/tasks', json={'title': 'Task B'})
    res = client.get('/tasks')
    assert len(res.get_json()) == 2

def test_get_task_by_id(client):
    client.post('/tasks', json={'title': 'Find me'})
    res = client.get('/tasks/1')
    assert res.status_code == 200
    assert res.get_json()['title'] == 'Find me'

def test_get_task_not_found(client):
    res = client.get('/tasks/999')
    assert res.status_code == 404

def test_get_tasks_filter_by_status(client):
    client.post('/tasks', json={'title': 'Pending task', 'status': 'pending'})
    client.post('/tasks', json={'title': 'Done task',    'status': 'done'})
    res = client.get('/tasks?status=done')
    data = res.get_json()
    assert len(data) == 1
    assert data[0]['status'] == 'done'

# ── UPDATE ───────────────────────────────────────────

def test_update_task_title(client):
    client.post('/tasks', json={'title': 'Old title'})
    res = client.put('/tasks/1', json={'title': 'New title'})
    assert res.status_code == 200
    assert res.get_json()['title'] == 'New title'

def test_update_task_status(client):
    client.post('/tasks', json={'title': 'Update status'})
    res = client.put('/tasks/1', json={'status': 'done'})
    assert res.get_json()['status'] == 'done'

def test_update_task_not_found(client):
    res = client.put('/tasks/999', json={'title': 'Ghost'})
    assert res.status_code == 404

def test_update_task_invalid_status(client):
    client.post('/tasks', json={'title': 'Some task'})
    res = client.put('/tasks/1', json={'status': 'invalid_val'})
    assert res.status_code == 400

# ── DELETE ───────────────────────────────────────────

def test_delete_task_success(client):
    client.post('/tasks', json={'title': 'Delete me'})
    res = client.delete('/tasks/1')
    assert res.status_code == 200
    assert 'deleted' in res.get_json()['message']

def test_delete_task_not_found(client):
    res = client.delete('/tasks/999')
    assert res.status_code == 404

def test_delete_removes_from_db(client):
    client.post('/tasks', json={'title': 'Gone soon'})
    client.delete('/tasks/1')
    res = client.get('/tasks/1')
    assert res.status_code == 404
