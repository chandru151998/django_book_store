from rest_framework.views import APIView
from user.utils import get_response, verify_user_token
from .models import Cart
from cart.serializers import CartSerializer
import logging

logging.basicConfig(filename='book_store.log', encoding='utf-8', level=logging.DEBUG)


class CartView(APIView):
    @verify_user_token
    def post(self, request):
        """Function to create cart"""
        try:
            serializer = CartSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return get_response(message="Cart added", data=serializer.data, status=201)
        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)

    @verify_user_token
    def get(self, request):
        """Function to view the cart data"""
        try:
            cart = Cart.objects.get(user=request.data.get("user"), status=False)
            serializer = CartSerializer(cart)
            return get_response(data=serializer.data, status=200)
        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)

    @verify_user_token
    def delete(self, request):
        """Function to delete the cart"""
        try:
            cart = Cart.objects.get(id=request.data.get('id'), user_id=request.data.get("user_id"))
            cart.delete()
            return get_response(status=204)
        except Exception as e:
            logging.exception(e)
            return get_response(message=str(e), status=400)


class CheckoutAPI(APIView):
    @verify_user_token
    def put(self, request):
        """method to update the purchase status of the user"""
        user = Cart.objects.get(user=request.data.get("user"), status=False)
        if user is not None:
            user.status = True
            user.save()
        return get_response(status=200)
