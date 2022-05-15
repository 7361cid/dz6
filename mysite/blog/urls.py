from django.urls import path

from .views import QuestionListView, QuestionDetailView, QuestionCreateView


urlpatterns = [
    path(r'question_list/', QuestionListView.as_view(), name='question_list'),
    path(r'question_list/<int:pk>/', QuestionDetailView.as_view(), name='question'),
    path('question_list/add/', QuestionCreateView.as_view(), name='question_new'),
]
