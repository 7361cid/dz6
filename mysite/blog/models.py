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


def change_rating(question_pk, vote):
    question = Question.objects.get(pk=question_pk)
    if vote:
        question.rating += 1
    elif vote is False:
        question.rating -= 1

    question.save()


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question_pk = models.IntegerField()
    vote = models.BooleanField(null=True)

    class Meta:
        unique_together = ['user', 'question_pk']

    def save(self, question_pk, *args, **kwargs):
        self.question_pk = question_pk
        super(Vote, self).save(*args, **kwargs)

    def set_vote(self, question_pk, vote=None):
        if vote is not None:
            self.vote = vote

        self.save(question_pk)
        print(f"LOG VOTE self.question_pk {self.question_pk} \n\n self.user {self.user} \n\n  "
              f"self.vote {self.vote} \n\n")

        change_rating(question_pk=question_pk, vote=self.vote)
