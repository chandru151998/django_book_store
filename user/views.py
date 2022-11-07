import logging
from django.contrib.auth import authenticate, login
from .serializers import RegistrationSerializer
from rest_framework.views import APIView
from .utils import get_response

logging.basicConfig(filename='book_store.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


class UserRegistration(APIView):
    """Class to register the user"""
    def post(self, request):
        """Method to register the user"""
        try:
            serializer = RegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return get_response(data=serializer.data, status=201)

        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)


class UserLogin(APIView):
    """Class to login the user"""
    def post(self, request):
        """Method to login the user"""
        try:
            user = authenticate(**request.data)
            if user is not None:
                login(request, user)
                return get_response(message='Login Successful', status=202)
            return get_response(status=406)

        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)
