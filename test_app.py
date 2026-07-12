import os
import tempfile
import pytest

# Create a temporary database before importing app
db_fd, db_path = tempfile.mkstemp()
os.environ["TODO_DB_PATH"] = db_path

from app import app, init_db, get_todos

app.config["TESTING"] = True


@pytest.fixture
def client():
    init_db()

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"To-Do List" in response.data


def test_add_todo(client):
    response = client.post(
        "/home",
        data={"todo_name": "Learn GitHub Actions"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Learn GitHub Actions" in response.data


def test_toggle_todo(client):
    client.post(
        "/home",
        data={"todo_name": "Task 1"},
        follow_redirects=True,
    )

    todo_id = get_todos()[0]["id"]

    response = client.post(
        f"/checked/{todo_id}",
        follow_redirects=True,
    )

    assert response.status_code == 200


def test_edit_todo(client):
    client.post(
        "/home",
        data={"todo_name": "Old Task"},
        follow_redirects=True,
    )

    todo_id = get_todos()[0]["id"]

    response = client.post(
        f"/edit/{todo_id}",
        data={"todo_name": "New Task"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"New Task" in response.data


def test_delete_todo(client):
    client.post(
        "/home",
        data={"todo_name": "Delete Me"},
        follow_redirects=True,
    )

    todo_id = get_todos()[0]["id"]

    response = client.post(
        f"/delete/{todo_id}",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Delete Me" not in response.data
