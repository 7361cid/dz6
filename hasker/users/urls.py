from django.urls import path
from .views import Signup, Login, logout_user, updateuser, index

urlpatterns = [
    path("signup/", Signup.as_view(), name="signup"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path('/<int:pk>/', updateuser, name='user'),
    path("", index, name='home'),
    path("home/<int:pk>/", index, name='home'),
    path("home/<int:pk>/<int:sort>/", index, name='home'),
    path("home/<str:tag>/", index, name='home'),
]
