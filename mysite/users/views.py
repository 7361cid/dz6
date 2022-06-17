from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from .models import CustomUser
from blog.models import Question, Answer


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "profile_pic")


class SignUp(CreateView):
    form_class = RegisterForm
    template_name = 'registration\\signup.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        ctx = super(SignUp, self).get_context_data(**kwargs)
        ctx['questions_trends'] = Question.objects.order_by('-rating', '-date')[:20]
        return ctx


def login_user(request):
    logout(request)
    csrf_token = get_token(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    questions_trends = Question.objects.order_by('-rating', '-date')[:20]
    return render(None, 'registration\\login.html', {'csrf_token': csrf_token,
                                                     'questions_trends': questions_trends})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        exclude = ('username', 'password', 'first_name', 'is_superuser', 'date_joined', 'user_permissions',
                   'last_name', 'is_staff', 'is_active', 'last_login', 'groups')


def updateuser(request, pk):
    page_user = get_object_or_404(CustomUser, id=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            if form.data['email']:
                page_user.email = form.cleaned_data['email']
                page_user.save()
            if form.data['profile_pic']:
                page_user.profile_pic = form.cleaned_data['profile_pic']
                page_user.save()
            render(request, 'user_profile.html', {'form': form, 'page_user': page_user})
    else:
        form = UserUpdateForm()
    questions_trends = Question.objects.order_by('-rating', '-date')[:20]
    return render(request, 'user_profile.html', {'form': form, 'page_user': page_user,
                                                 'questions_trends': questions_trends})


def index(request, pk=1, tag='', sort=1):
    search = request.GET.get('q')
    if sort == 1:
        order_by = "-date"
    else:
        order_by = "-rating"
    if tag:
        questions = Question.objects.filter(Q(tag__tag__icontains=tag)).order_by(order_by)
    else:
        if search:
            if search.startswith("tag:"):
                tag = search.split('tag:')[-1]
                questions = Question.objects.filter(Q(tag__tag__icontains=tag)).order_by(order_by)
            else:
                questions = Question.objects.filter(Q(title__icontains=search) |
                                                    Q(content__icontains=search)).order_by(order_by)
        else:
            questions = Question.objects.all().order_by(order_by)

    paginator = Paginator(questions, 20)  # Show 20 contacts per page.
    questions_trends = Question.objects.order_by('-rating', '-date')[:20]
    answers = {}
    for q in questions:
        answers[q.pk] = len(Answer.objects.filter(question_pk=q.pk))

    context = {
        'answers': answers,  # Количество овтетов для каждого вопроса
        'questions': questions,
        'questions_trends': questions_trends,
        'paginator': paginator.page(pk)
    }

    return render(request, 'home.html', context=context)
