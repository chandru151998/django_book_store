import jwt
from rest_framework .views import Response
from django.conf import settings
from user.models import User
import logging

logging.basicConfig(filename='book_store.log', encoding='utf-8', level=logging.DEBUG)


def get_response(data=None, message="", status=200):
    if data is None:
        data = {}
    message_dict = {200: "OK", 201: "Created", 202: "Accepted", 405: "Method not allowed", 406: "invalid credentials"}
    if message == "":
        message = message_dict.get(status)
    return Response({"data": data, "message": message, "status": status}, status=status)


class JWT:
    def encode(self, data):
        if not isinstance(data, dict):
            raise Exception("Data should be a dictionary")
        return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHMS)

    def decode(self, token):
        try:
            return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHMS])
        except jwt.exceptions.PyJWTError as e:
            raise e


def get_user(request):
    token = request.headers.get("Token")
    if not token:
        raise Exception("Token not found")
    decoded = JWT().decode(token)
    if not decoded:
        raise Exception("Token Authentication required")
    user = User.objects.get(id=decoded.get("user_id"))
    if not user:
        raise Exception("Invalid user")
    if not user.is_verified:
        raise Exception("User not verified")
    return decoded, user


def verify_user_token(function):
    def wrapper(self, request, *args, **kwargs):
        try:
            payload, user = get_user(request)
            request.data.update({"user": payload.get("user_id")})
        except Exception as e:
            logging.exception(e)
        return function(self, request, *args, **kwargs)
    return wrapper


def verify_superuser_token(function):
    def wrapper(self, request, *args, **kwargs):
        try:
            payload, user = get_user(request)
            if not user.is_superuser:
                raise Exception("User unauthorized to perform the task")
            request.data.update({"user": payload.get("user_id")})
        except Exception as e:
            logging.exception(e)
        return function(self, request, *args, **kwargs)
    return wrapper


