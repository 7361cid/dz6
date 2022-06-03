from django.urls import path
from .views import SignUp, ShowProfilePageView, index

urlpatterns = [
    path("signup/", SignUp.as_view(), name="signup"),
    path('/<int:pk>/', ShowProfilePageView.as_view(), name='user'),
    path("", index, name='home'),
    path("home/<int:pk>/", index, name='home'),
    path("home/<str:tag>/", index, name='home'),
]
