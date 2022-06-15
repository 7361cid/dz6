from django.views.generic.edit import CreateView
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms

from .models import CustomUser
from blog.models import Question, Answer


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "profile_pic")


class SignUp(CreateView):
    form_class = RegisterForm
    template_name = 'registration\signup.html'
    success_url = reverse_lazy('login')


class UserUpdateForm(forms.Form):
    email = forms.EmailField(required=False)
    profile_pic = forms.ImageField(required=False)

    def form_valid(self, form):
        print(f"LOG {form}")
        form.save()


def updateuser(request, pk):
    # if form is submitted
    page_user = get_object_or_404(CustomUser, id=pk)
    if request.method == 'POST':
        # will handle the request later
        form = UserUpdateForm(request.POST)
        print(f"LOG {form.data}")

        if form.is_valid():
            render(request, 'user_profile.html', {'form': form, 'page_user': page_user})
    else:
        # creating a new form
        form = UserUpdateForm()

    # returning form
    return render(request, 'user_profile.html', {'form': form, 'page_user': page_user})


def index(request, pk=1, tag=''):
    search = request.GET.get('q')
    if tag:
        print(f"LOG {tag}")
        questions = Question.objects.filter(Q(tag__tag__icontains=tag)).order_by('-rating', '-date')
    else:
        if search:
            if search.startswith("tag:"):
                tag = search.split('tag:')[-1]
                questions = Question.objects.filter(Q(tag__tag__icontains=tag)).order_by('-rating', '-date')
            else:
                questions = Question.objects.filter(Q(title__icontains=search) |
                                                    Q(content__icontains=search)).order_by('-rating', '-date')
        else:
            questions = Question.objects.all().order_by('-rating', '-date')

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
