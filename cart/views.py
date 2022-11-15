from django.forms import model_to_dict
from rest_framework.views import APIView
from book.models import Book
from user.utils import get_response, verify_user_token
from .models import Cart, CartItem
import logging

logging.basicConfig(filename='book_store.log', encoding='utf-8', level=logging.DEBUG)


class CartView(APIView):
    @verify_user_token
    def post(self, request):
        """Function to create cart"""
        try:
            cart_list = Cart.objects.filter(user_id=request.data.get("user"), status=False)
            if len(cart_list) == 0:
                cart = Cart.objects.create(user_id=request.data.get('user'))
            else:
                cart = cart_list.first()
            for book_dict in request.data.get('books'):
                book = Book.objects.get(id=book_dict.get('book_id'))
                for _ in range(book_dict.get('quantity')):
                    CartItem.objects.create(book_id=book.id, price=book.price, user_id=request.data.get("user"),
                                            cart_id=cart.id)
            cart_items = [model_to_dict(item) for item in cart.cartitem_set.all()]
            return get_response(
                data={"id": cart.id, 'item': cart_items, "total_price": cart.total_price, "status": cart.status},
                status=201)
        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)

    def get(self, request):
        """Function to view the cart data"""
        try:
            cart_items = CartItem.objects.all()
            cart_list = [{"Book id": cart_data.book.id, "Book": cart_data.book.title, "Price": cart_data.price,
                          "status": cart_data.cart.status} for cart_data in cart_items]
            return get_response(data=cart_list, status=200)
        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)

    @verify_user_token
    def delete(self, request):
        """Function to delete the cart"""
        try:
            cart = Cart.objects.get(id=request.data.get('cart_id'), user_id=request.data.get("user_id"))
            cart.delete()
            return get_response(status=204)
        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)
