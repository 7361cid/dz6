from django.urls import path

from .views import QuestionView, QuestionCreateView, VoteForQuestion, VoteForAnswer, RightAnswer


urlpatterns = [
    path(r'question_list/<int:pk>/', QuestionView.as_view(), name='question'),
    path(r'question_list/<int:pk>/<int:page>', QuestionView.as_view(), name='question'),
    path('question_list/add/', QuestionCreateView.as_view(), name='question_new'),
    path('question_list/<int:pk>/vote_for_question/', VoteForQuestion.as_view(), name='vote_for_question'),
    path('question_list/<int:pk>/vote_for_answer/<int:pk2>', VoteForAnswer.as_view(), name='vote_for_answer'),
    path('question_list/<int:pk>/make_answer_right/<int:pk2>', RightAnswer.as_view(), name='make_answer_right'),
]
