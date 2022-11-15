# from rest_framework import serializers
# from .models import CartItem, Cart
# from book.models import Book
# import logging
#
# logging.basicConfig(filename='book_store.log', encoding='utf-8', level=logging.DEBUG)
#
#
# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartItem
#         fields = ['id', 'price', 'quantity', 'book', 'user', 'cart']
#
#
# class CartSerializer(serializers.ModelSerializer):
#     book = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Book.objects.all())
#
#     class Meta:
#         model = Cart
#         fields = ['id', 'total_price', 'total_quantity', 'status', 'user', 'quantity', 'book']
#
#     def create(self, validated_data):
#         user = validated_data.get('user')
#         book = validated_data.get('book')
#         cart_list = Cart.objects.filter(user=user)
