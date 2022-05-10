from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import CustomUser
from blog.models import Question
# Создаем здесь представления.


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "profile_pic")


class SignUp(CreateView):
    form_class = RegisterForm
    template_name = 'registration\signup.html'
    success_url = reverse_lazy('login')


class ShowProfilePageView(DetailView):
    model = CustomUser
    template_name = 'user_profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(CustomUser, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    questions = Question.objects.all()

    context = {
        'questions': questions,
    }

    return render(request, 'home.html', context=context)
