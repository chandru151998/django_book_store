from drf_yasg import openapi
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'quantity', 'user']
        swagger_schema_fields = {"required": ['title', 'author', 'price', 'quantity', 'user'], "type": openapi.TYPE_OBJECT,
                                 "properties": {
                                     "title": openapi.Schema(
                                         title="title",
                                         type=openapi.TYPE_STRING,
                                     ),
                                     "author": openapi.Schema(
                                         title="author",
                                         type=openapi.TYPE_STRING,
                                     ),
                                     "price": openapi.Schema(
                                         title="price",
                                         type=openapi.TYPE_INTEGER,
                                     ),
                                     "quantity": openapi.Schema(
                                         title="quantity",
                                         type=openapi.TYPE_INTEGER,
                                     ),
                                     "user": openapi.Schema(
                                         title="user",
                                         type=openapi.TYPE_INTEGER,
                                     )
                                 }}
