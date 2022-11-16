from django.db import models
from user.models import User
from book.models import Book


class Cart(models.Model):
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    @property
    def total_price(self):
        price = sum([item.price for item in self.cartitem_set.all()])
        return price

    @property
    def cartitem(self):
        try:
            return self.cartitem_set.all()
        except Exception:
            return []


class CartItem(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    date_of_purchase = models.DateTimeField(auto_now_add=True)
