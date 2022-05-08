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
    datetime = models.DateTimeField(u'Дата создания')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return "/blog/question_list/%i/" % self.id
