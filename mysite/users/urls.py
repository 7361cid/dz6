from django.urls import path
from .views import SignUp, login_user, logout_user, updateuser, index

urlpatterns = [
    path("signup/", SignUp.as_view(), name="signup"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path('/<int:pk>/', updateuser, name='user'),
    path("", index, name='home'),
    path("home/<int:pk>/", index, name='home'),
    path("home/<int:sort>/", index, name='home'),
    path("home/<str:tag>/", index, name='home'),

]
