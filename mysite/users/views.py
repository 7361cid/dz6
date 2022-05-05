from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import CustomUser

# Создаем здесь представления.


def home(request):
    return render(request, "home.html")


class SignUp(CreateView):
    model = CustomUser
    template_name = 'registration\signup.html'
    fields = '__all__'

