import pytest
from django.urls import reverse
REGISTER_URL = reverse('register')
LOGIN_URL = reverse('login')


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='chandru', first_name="Chandru", last_name="K",
                                                 email='c@gmail.com', password='1234', location='bng',
                                                 phone_no=1233, is_verified=True)


@pytest.fixture
def user_data():
    return {'username': 'chandru',
            'first_name': 'Chandru', 'last_name': 'K',
            'email': 'c@gmail.com',
            'password': 'c',
            'location': 'b',
            'phone_no': 1234}


@pytest.fixture
def user_data_error():
    return {'usernam': 'chandru',
            'first_name': 'Chandru', 'last_name': 'K',
            'email': 'c@gmail.com',
            'password': 'c',
            'location': 'b',
            'phone_no': 1234}


@pytest.fixture
def user_login_data():
    return {'username': 'chandru', 'password': '1234'}


@pytest.fixture
def user_login_data_error():
    return {'username': 'chandruu', 'password': '1234'}


class TestUserLoginAndRegister:
    @pytest.mark.django_db
    def test_user_registration_successfully(self, client, django_user_model, user_data):
        response = client.post(REGISTER_URL, user_data, content_type="application/json")
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_user_registration_unsuccessfully(self, client, django_user_model, user_data_error):
        response = client.post(REGISTER_URL, user_data_error, content_type="application/json")
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_user_login_successfully(self, client, user_login_data, user):
        response = client.post(LOGIN_URL, user_login_data, content_type="application/json")
        assert response.status_code == 202

    @pytest.mark.django_db
    def test_user_login_unsuccessfully(self, client, user, user_login_data_error):
        response = client.post(LOGIN_URL, user_login_data_error, content_type="application/json")
        assert response.status_code == 400
