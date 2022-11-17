import logging
from django.conf import settings
from django.core.mail import send_mail
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import User
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.views import APIView
from .utils import get_response, JWT
from rest_framework.reverse import reverse

logging.basicConfig(filename='book_store.log', encoding='utf-8', level=logging.DEBUG)


class UserRegistration(APIView):
    """Class to register the user"""

    @swagger_auto_schema(request_body=RegistrationSerializer, responses={201: 'Created', 400: 'BAD REQUEST'})
    def post(self, request):
        """Method to register the user"""
        try:
            serializer = RegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token = JWT().encode(data={"username": serializer.data.get("username")})
            send_mail(
                subject='Verify token',
                message=settings.BASE_URL + reverse('verify_token', kwargs={"token": token}),
                from_email=None,
                recipient_list=[serializer.data.get("email")],
            )
            return get_response(data=serializer.data, status=201)
        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)


class UserLogin(APIView):
    """Class to login the user"""

    @swagger_auto_schema(request_body=LoginSerializer, responses={202: 'Login Successful', 400: 'BAD REQUEST'})
    def post(self, request):
        """Method to login the user"""
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token = JWT().encode({"user_id": serializer.data.get("id")})
            return get_response(data=token, message='Login Successful', status=202)
        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)


class VerifyToken(APIView):
    def get(self, request, token=None):
        try:
            decoded = JWT().decode(token)
            user = User.objects.get(username=decoded.get("username"))
            if not user:
                raise Exception("Invalid user")
            user.is_verified = True
            user.save()
            return get_response(message="Token verified")
        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)
