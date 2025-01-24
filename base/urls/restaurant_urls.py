from django.urls import path
from base.views import restaurant_views as views


urlpatterns = [
    # Restaurants
    path('', views.getRestaurants, name='restaurants'),
    path('owners/', views.getRestaurantByOwner, name='owner-restaurants'),
    path('create/', views.createRestaurant, name='restaurant-create'),
    path('upload/', views.uploadImage, name='image-upload'),
    path('<str:pk>/', views.getRestaurant, name='restaurant'),
    path('update/<str:pk>/', views.updateRestaurant, name='restaurant-update'),
    
    # Menus                   
    path('menus/all/', views.getAllMenus, name='all-menus'),
    path('menus/create/', views.createMenu, name='create-menu'),
    path('menus/update/<str:pk>/', views.updateMenu, name='update-menu'),
    
    # Items
    path('menus/item/create/<str:menu_id>/', views.createMenuItem, name='create-menus-items'),
    path('menus/item/update/<str:menu_id>/<str:item_id>/', views.updateMenuItem, name='update-menus-items'),
    path('menus/employee/', views.getRestaurantMenus, name='employee-menus'),
]