import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Book
from rest_framework.views import APIView
from book.serializers import BookSerializer
from user.utils import get_response, verify_superuser_token
from .utils import Cache

logging.basicConfig(filename='book_store.log', encoding='utf-8', level=logging.DEBUG)


class BookAPI(APIView):
    """Class to add, update, delete and view the books"""
    @swagger_auto_schema(request_body=BookSerializer, responses={201: 'Created', 400: 'BAD REQUEST'})
    @verify_superuser_token
    def post(self, request):
        """Function to add book"""
        try:
            print(request.data)
            serializer = BookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            Cache().add_book(request.data.get("user"), serializer.data)
            return get_response(message="Book added", data=serializer.data, status=201)

        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)

    @swagger_auto_schema(responses={200: 'Books list', 400: 'BAD REQUEST'})
    def get(self, request):
        """Function to view all books"""
        try:
            # book_list = Book.objects.all()
            # serializer = BookSerializer(book_list, many=True)
            book = Cache().get_book(user=request.data.get("user"))
            return get_response(message="Books list", data=book.values(), status=200)
        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                 'title': openapi.Schema(type=openapi.TYPE_STRING),
                                                                 'author': openapi.Schema(type=openapi.TYPE_STRING),
                                                                 'price': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                 'quantity': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                 'user': openapi.Schema(type=openapi.TYPE_INTEGER), },
                                                     required=['id', 'user']),
                         responses={201: 'Book updated', 400: 'BAD REQUEST'})
    @verify_superuser_token
    def put(self, request):
        """Function to update book details"""
        try:
            book_object = Book.objects.get(id=request.data.get("id"), user=request.data.get("user"))
            serializer = BookSerializer(book_object, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            Cache().update_book(request.data.get("user"), serializer.data)
            return get_response(message="Book updated", data=serializer.data, status=201)
        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                 'user': openapi.Schema(type=openapi.TYPE_INTEGER), },
                                                     required=['id', 'user']),
                         responses={204: 'Book deleted', 400: 'BAD REQUEST'})
    @verify_superuser_token
    def delete(self, request):
        """Function to delete a book"""
        try:
            book_object = Book.objects.get(id=request.data.get("id"), user=request.data.get("user"))
            book_object.delete()
            Cache().delete_note(request.data.get("user"), request.data.get("id"))
            return get_response(message="Book deleted", status=204)
        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)
