from django.urls import path

from .views import question_with_answers_view, QuestionCreateView, vote_for_question, \
    make_answer_right


urlpatterns = [
    path(r'question_list/<int:pk>/', question_with_answers_view, name='question'),
    path('question_list/add/', QuestionCreateView.as_view(), name='question_new'),
    path('question_list/<int:pk>/vote_for_question/', vote_for_question, name='vote_for_question'),
    path('question_list/<int:pk>/make_answer_right/<int:pk2>', make_answer_right, name='make_answer_right'),
]
