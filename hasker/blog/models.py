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
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)
    tag2 = models.ForeignKey(Tag, on_delete=models.PROTECT, related_name='tag2', blank=True, null=True)
    tag3 = models.ForeignKey(Tag, on_delete=models.PROTECT, related_name='tag3', blank=True, null=True)
    rating = models.IntegerField(default=0)

    def get_absolute_url(self):
        return f"/blog/question_list/{self.id}/"

    def get_top20(self):
        return Question.objects.order_by('-rating', '-date')[:20]


class Answer(models.Model):
    """
     Ответ – содержание, автор, дата написания, флаг правильного ответа.
    """
    content = models.TextField(max_length=10000)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    right = models.BooleanField(default=0)
    question_pk = models.IntegerField()
    rating = models.IntegerField(default=0)


def change_rating(question_pk, vote):
    question = Question.objects.get(pk=question_pk)
    if vote:
        question.rating += 1
    elif vote is False:
        question.rating -= 1
    question.save()


def change_rating_answer(answer_pk, vote):
    answer = Answer.objects.get(pk=answer_pk)
    if vote:
        answer.rating += 1
    elif vote is False:
        answer.rating -= 1
    answer.save()


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

        change_rating(question_pk=question_pk, vote=self.vote)


class VoteAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer_pk = models.IntegerField()
    vote = models.BooleanField(null=True)

    class Meta:
        unique_together = ['user', 'answer_pk']

    def save(self, answer_pk, *args, **kwargs):
        self.answer_pk = answer_pk
        super(VoteAnswer, self).save(*args, **kwargs)

    def set_vote(self, answer_pk, vote=None):
        if vote is not None:
            self.vote = vote

        self.save(answer_pk)

        change_rating_answer(answer_pk=answer_pk, vote=self.vote)
