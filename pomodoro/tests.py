import json

from django.contrib.auth.models import User
from rest_framework.test import APIClient
import pytest

from pomodoro.models import Pomodoro


@pytest.fixture
def users(request):
    for username in 'bob tim'.split():
        User.objects.create_user(
            username, f"{username}@mail.com", "password")
    return User.objects.all()


@pytest.fixture
def pomos(request):
    for notes, user_id in zip(
        ("wrote a blog post", "read Python in a Nutshell"),
        (1, 2)
    ):
        Pomodoro.objects.create(
            notes=notes, user_id=user_id)


@pytest.fixture
def client(request):
    return APIClient()


@pytest.fixture
def login_user1(request, users, client):
    client.login(username=users[0].username, password="password")


@pytest.fixture
def login_user2(request, users, client):
    client.login(username=users[1].username, password="password")


def test_get_all_pomodori(client, users, pomos):
    ret = client.get('/')

    rows = ret.data['results']
    assert len(rows) == 2

    # ordered descending
    assert rows[0]["notes"] == "read Python in a Nutshell"
    assert rows[1]["notes"] == "wrote a blog post"

    assert rows[0]["added"] > rows[1]["added"]


def test_get_individual_pomodoro(client, users, pomos):
    ret = client.get('/1/')
    assert ret.data["notes"] == "wrote a blog post"
    ret = client.get('/2/')
    assert ret.data["notes"] == "read Python in a Nutshell"


def test_post_new_pomodoro(client, pomos, login_user1):
    body = {'notes': 'produced a bite', 'user_id': 1}
    ret = client.post('/', json.dumps(body),
                      content_type='application/json')
    assert ret.status_code == 201
    ret = client.get('/')
    rows = ret.data['results']
    assert len(rows) == 3
    # newest first
    assert rows[0]['notes'] == "produced a bite"
    assert rows[0]['user'] == "bob"


def test_update_pomodoro(client, pomos, login_user1):
    ret = client.get('/')
    rows = ret.data['results']
    assert len(rows) == 2
    assert rows[0]['notes'] == "read Python in a Nutshell"
    assert rows[1]['notes'] == "wrote a blog post"
    body = {'notes': 'read Fluent Python', 'user_id': 1}
    ret = client.put('/2/', json.dumps(body),
                     content_type='application/json')
    # cannot update pomodoro owned by other user
    assert ret.status_code == 403
    ret = client.put('/1/', json.dumps(body),
                     content_type='application/json')
    assert ret.status_code == 200
    ret = client.get('/')
    rows = ret.data['results']
    assert len(rows) == 2
    assert rows[0]['notes'] == "read Python in a Nutshell"
    assert rows[1]['notes'] == "read Fluent Python"


def test_delete_pomodoro_user1(client, users, pomos, login_user1):
    ret = client.delete('/2/')
    assert ret.status_code == 403
    ret = client.delete('/1/')
    assert ret.status_code == 204
    ret = client.get('/')
    rows = ret.data['results']
    assert len(rows) == 1
    assert rows[0]['notes'] == "read Python in a Nutshell"


def test_delete_pomodoro_user2(client, users, pomos, login_user2):
    # changed login so now I cannot delete bob's quote
    ret = client.delete('/1/')
    assert ret.status_code == 403
    ret = client.delete('/2/')
    assert ret.status_code == 204
    ret = client.get('/')
    rows = ret.data['results']
    assert len(rows) == 1
    assert rows[0]['notes'] == "wrote a blog post"
