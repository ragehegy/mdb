from django.urls import path
from user.views import RegisterView
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path("register", 
        RegisterView.as_view(), 
        name="register"),
    path("login", 
        auth_views.LoginView.as_view(), 
        name="login"),
    path("logout", 
        auth_views.LogoutView.as_view(), 
        name="logout"),
]