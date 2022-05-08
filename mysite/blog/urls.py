from django.urls import path

from .views import QuestionListView, QuestionDetailView


urlpatterns = [
    path(r'question_list/', QuestionListView.as_view(), name='question_list'),
    path(r'question_list/<int:pk>/', QuestionDetailView.as_view(), name='question'),
]
