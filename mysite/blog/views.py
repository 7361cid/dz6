from .models import Question
from django.views.generic import ListView, DetailView


class QuestionListView(ListView):
    model = Question
    template_name = 'question_list.html'


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'question.html'
