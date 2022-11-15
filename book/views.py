import logging
from .models import Book
from rest_framework.views import APIView
from book.serializers import BookSerializer
from user.utils import get_response, verify_superuser_token

logging.basicConfig(filename='book_store.log', encoding='utf-8', level=logging.DEBUG)


class BookAPI(APIView):
    """Class to add, update, delete and view the books"""
    @verify_superuser_token
    def post(self, request):
        """Function to add book"""
        try:
            serializer = BookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return get_response(message="Book added", data=serializer.data, status=201)
        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)

    def get(self, request):
        """Function to view all books"""
        try:
            book_list = Book.objects.all()
            serializer = BookSerializer(book_list, many=True)
            return get_response(message="Books list", data=serializer.data, status=200)
        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)

    @verify_superuser_token
    def put(self, request):
        """Function to update book details"""
        try:
            book_object = Book.objects.get(id=request.data.get("id"), user=request.data.get("user"))
            serializer = BookSerializer(book_object, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return get_response(message="Book updated", data=serializer.data, status=201)
        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)

    @verify_superuser_token
    def delete(self, request):
        """Function to delete a book"""
        try:
            book_object = Book.objects.get(id=request.data.get("id"), user=request.data.get("user"))
            book_object.delete()
            return get_response(message="Book deleted", status=204)
        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)
