from django.db import models

from users.models import CustomUser
from django.conf import settings


class Tag(models.Model):
    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.tag


class Question(models.Model):
    """
    Вопрос – заголовоĸ, содержание, автор, дата создания, тэги.
    """
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=10000)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def get_absolute_url(self):
        return "/blog/question_list/%i/" % self.id


class Answer(models.Model):
    """
     Ответ – содержание, автор, дата написания, флаг правильного ответа.
    """
    content = models.TextField(max_length=10000)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    right = models.BooleanField(default=0)
    question_pk = models.IntegerField()


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question_pk = models.IntegerField()
    vote = models.BooleanField(null=True)

    class Meta:
        unique_together = ['user', 'question']

    def set_vote(self, vote=None):
        if vote is not None:
            self.vote = vote

        self.save()

        if self.vote:
            self.question.rating += 1
        elif vote is False:
            self.question.rating -= 1

        self.question.rating.save()
