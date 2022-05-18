from django.db import models

from users.models import CustomUser


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
