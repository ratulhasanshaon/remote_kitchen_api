from django.urls import path
from base.views import order_views as views

urlpatterns = [
    # for owner and employee
    path('restaurant_orders/', views.getResOrders, name='restaurant-orders'),
    path('myorders/', views.getMyOrders, name='myorders'),

    # for user
    path('add/', views.addOrderItems, name='orders-add'),
    path('<str:pk>/', views.getOrderById, name='user-order'),
    path('<str:pk>/make_payment/', views.makePayment, name='payment'),
]