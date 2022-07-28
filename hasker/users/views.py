from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.db.models import Q
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views.generic.base import View
from django.views.generic.list import ListView

from .models import CustomUser
from .forms import RegisterForm, UserUpdateForm
from blog.models import Question, Answer


class Signup(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        questions_trends = Question.get_top20()
        return render(request, 'registration\\signup.html', {'form': form, 'questions_trends': questions_trends})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = CustomUser.objects.get(username=username)
            user.profile_avatar = request.FILES['profile_avatar']
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        questions_trends = Question.get_top20()
        return render(request, 'registration\\signup.html', {'form': form, 'questions_trends': questions_trends})


class Login(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        csrf_token = get_token(request)
        questions_trends = Question.get_top20()
        return render(None, 'registration\\login.html', {'csrf_token': csrf_token,
                                                         'questions_trends': questions_trends})

    def post(self, request, *args, **kwargs):
        csrf_token = get_token(request)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
        questions_trends = Question.get_top20()
        return render(None, 'registration\\login.html', {'csrf_token': csrf_token,
                                                         'questions_trends': questions_trends})


def logout_user(request):
    logout(request)
    return redirect('/')


class UpdateUser(View):
    def get(self, request, pk, *args, **kwargs):
        page_user = get_object_or_404(CustomUser, id=pk)
        form = UserUpdateForm()
        questions_trends = Question.get_top20()
        context = {'form': form, 'page_user': page_user, 'questions_trends': questions_trends}
        if request.user.is_authenticated:
            context['user_avatar'] = request.user.get_avatar()
        context['page_user_avatar'] = page_user.get_avatar()
        return render(request, 'user_profile.html', context)

    def post(self, request, pk, *args, **kwargs):
        page_user = get_object_or_404(CustomUser, id=pk)
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            if form.data['email']:
                page_user.email = form.cleaned_data['email']
                page_user.save()
            if "profile_avatar" in request.FILES.keys():
                page_user.profile_avatar = request.FILES['profile_avatar']
                page_user.save()

            render(request, 'user_profile.html', {'form': form, 'page_user': page_user})
        questions_trends = Question.get_top20()
        context = {'form': form, 'page_user': page_user, 'questions_trends': questions_trends}
        if request.user.is_authenticated:
            context['user_avatar'] = request.user.get_avatar()
        context['page_user_avatar'] = page_user.get_avatar()
        return render(request, 'user_profile.html', context)


class MainPage(ListView):
    paginate_by = 20
    model = Question

    def get(self, request, pk=1, tag='', sort=1, *args, **kwargs):
        search = request.GET.get('q')
        if sort == 1:
            order_by = "-date"
        else:
            order_by = "-rating"
        if tag:
            print(f"tag {tag}")
            questions = Question.objects.filter(Q(tags__tag__icontains=tag)).order_by(order_by)
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

        questions_trends = Question.get_top20()
        answers = {}
        for q in questions:
            answers[q.pk] = len(Answer.objects.filter(question_pk=q.pk))
        self.object_list = questions
        context = self.get_context_data()
        if pk > 1:
            context['page_obj'] = context['paginator'].page(pk)
        context['answers'] = answers  # Количество овтетов для каждого вопроса
        context['questions'] = questions
        context['questions_trends'] = questions_trends
        if request.user.is_authenticated:
            context['user_avatar'] = request.user.get_avatar()

        return render(request, 'home.html', context=context)
