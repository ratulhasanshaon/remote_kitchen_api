from django.urls import path
from base.views import user_views as views



urlpatterns = [
    
    path('login/', views.MyTokenObtainPairView.as_view(), 
        name='token_obtain_pair'),
    path('register/', views.registerUser, name='register'),

    path('profile/', views.getUserProfile, name='users-profile'),
    path('employee_profile/', views.getEmployeeProfile, name='employee-profile'),
    path('employee_profile/update/<str:pk>/', views.updateEmployeeProfile, name='update-employee-profile'),
    path('profile/update/', views.updateUserProfile, name='user-profile-update'),
    
    path('', views.getUsers, name='users'),
    path('<str:pk>/', views.getUserById, name='user'),

]
