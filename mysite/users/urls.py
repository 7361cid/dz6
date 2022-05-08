from django.urls import path
from .views import SignUp, ShowProfilePageView

urlpatterns = [
    path("signup/", SignUp.as_view(), name="signup"),
    path('/<int:pk>/', ShowProfilePageView.as_view(), name='user'),
]
