from django.urls import path
from .views import (
    CreateOrderView,
    OrderListView,
    OrderDetailView,
    UpdateOrderStatusView
)

urlpatterns = [
    path('create/', CreateOrderView.as_view()),
    path('', OrderListView.as_view()),
    path('<int:order_id>/', OrderDetailView.as_view()),
    path('update-status/<int:order_id>/', UpdateOrderStatusView.as_view()),
]