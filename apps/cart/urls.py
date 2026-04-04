from django.urls import path
from .views import CartView, UpdateCartItemView, RemoveCartItemView, ClearCartView, AddToCartView

urlpatterns = [
    path('', CartView.as_view()),
    path('add/', AddToCartView.as_view()),
    path('update/<int:item_id>/', UpdateCartItemView.as_view()),
    path('remove/<int:item_id>/', RemoveCartItemView.as_view()),
    path('clear/', ClearCartView.as_view()),
]