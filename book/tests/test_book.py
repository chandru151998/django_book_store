import pytest
import json
from django.urls import reverse

url = reverse('book')


@pytest.fixture
def get_token_header(django_user_model, client):
    user = django_user_model.objects.create_user(username='a', first_name="a", last_name="a",
                                                 email='a@gmail.com', password='1234', location='a',
                                                 phone_no=1234, is_verified=True, is_superuser=True)
    user.save()
    url = reverse('login')
    data = {'username': 'a', 'password': '1234'}
    response = client.post(url, data, content_type="application/json")

    json_data = json.loads(response.content)
    token = json_data['data']
    header = {'HTTP_TOKEN': token, "content_type": "application/json"}
    return user, header


@pytest.fixture
def book_details(get_token_header):
    user, header = get_token_header
    return {
        "title": "a",
        "author": "b",
        "price": 100,
        "quantity": 2,
        "user": user.id}


@pytest.fixture
def book_details_error(get_token_header):
    user, header = get_token_header
    return {
        "title": "a",
        "author": "b",
        "price": 100,
        "quantit": 2,
        "user": user.id}


@pytest.fixture
def book_update_data(client, get_token_header, book_details):
    user, header = get_token_header
    response = client.post(url, book_details, **header)
    json_data = json.loads(response.content)
    book_id = json_data['data']['id']
    return {'id': book_id,
            "title": "ab",
            "author": "c",
            "price": 120,
            "quantity": 2}


@pytest.fixture
def book_update_data_error(client, get_token_header, book_details):
    user, header = get_token_header
    response = client.post(url, book_details, **header)
    json_data = json.loads(response.content)
    book_id = json_data['data']['id']
    return {'id': "book",
            "title": "ab",
            "author": "c",
            "price": 120,
            "quantity": 4}


@pytest.fixture
def book_delete_data(client, get_token_header, book_details):
    user, header = get_token_header
    response = client.post(url, book_details, **header)
    json_data = json.loads(response.content)
    book_id = json_data['data']['id']
    data = {'id': book_id}
    return data


@pytest.fixture
def book_delete_data_error(client, get_token_header, book_details):
    user, header = get_token_header
    response = client.post(url, book_details, **header)
    json_data = json.loads(response.content)
    book_id = json_data['data']['id']
    data = {'id': 'book_id'}
    return data


class TestBooksAPI:

    @pytest.mark.django_db
    def test_response_as_create_book_successfully(self, client, get_token_header, book_details):
        user, header = get_token_header
        response = client.post(url, book_details, **header)
        json_data = json.loads(response.content)
        assert response.status_code == 201
        assert json_data['data']['title'] == 'a'

    @pytest.mark.django_db
    def test_response_as_create_book_unsuccessfully(self, client, get_token_header, book_details_error):
        user, header = get_token_header
        response = client.post(url, book_details_error, **header)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_response_as_get_books(self, client, get_token_header, book_details):
        user, header = get_token_header
        response = client.post(url, book_details, **header)
        assert response.status_code == 201
        response = client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_response_as_update_books_successfully(self, client, get_token_header, book_update_data):
        user, header = get_token_header
        response = client.put(url, book_update_data, **header)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_response_as_update_books_unsuccessfully(self, client, get_token_header, book_update_data_error):
        user, header = get_token_header
        response = client.put(url, book_update_data_error, **header)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_response_as_delete_books_successfully(self, client, get_token_header, book_delete_data):
        user, header = get_token_header
        response = client.delete(url, book_delete_data, **header)
        assert response.status_code == 204

    @pytest.mark.django_db
    def test_response_as_delete_books_successfully(self, client, get_token_header, book_delete_data):
        user, header = get_token_header
        response = client.delete(url, book_delete_data, **header)
        assert response.status_code == 204

    @pytest.mark.django_db
    def test_response_as_delete_books_unsuccessfully(self, client, get_token_header, book_delete_data_error):
        user, header = get_token_header
        response = client.delete(url, book_delete_data_error, **header)
        assert response.status_code == 400
