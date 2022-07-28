from django.urls import path
from .views import Signup, Login, Logout, UpdateUser, MainPage

urlpatterns = [
    path("signup/", Signup.as_view(), name="signup"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path('/<int:pk>/', UpdateUser.as_view(), name='user'),
    path("", MainPage.as_view(), name='home'),
    path("home/<int:pk>/", MainPage.as_view(), name='home'),
    path("home/<int:pk>/<int:sort>/", MainPage.as_view(), name='home'),
    path("home/<str:tag>/", MainPage.as_view(), name='home'),
]
