from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.BookAPI.as_view(), name='book'),
]
