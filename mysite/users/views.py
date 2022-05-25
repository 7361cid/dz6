from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q

from .models import CustomUser
from blog.models import Question


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


def index(request, pk=1):
    search = request.GET.get('q')
    if search:
        questions = Question.objects.filter(
            Q(title__icontains=search) | Q(content__icontains=search)
        )
    else:
        questions = Question.objects.all()
    paginator = Paginator(questions, 20)  # Show 20 contacts per page.
    questions_trends = Question.objects.order_by('-rating')[:20]
    context = {
        'questions': questions,
        'questions_trends': questions_trends,
        'paginator': paginator.page(pk)
    }

    return render(request, 'home.html', context=context)
