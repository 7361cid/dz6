from django.db import models, transaction
from django.urls import reverse
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
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0)

    def get_absolute_url(self):
        reverse('question', args=[self.id])
        return reverse('question', args=[self.id])

    @staticmethod
    def get_top20():
        return Question.objects.order_by('-rating', '-date')[:20]

    @staticmethod
    def change_rating(question_pk, vote):
        with transaction.atomic():
            question = Question.objects.get(pk=question_pk)
            if vote:
                question.rating += 1
            elif vote is False:
                question.rating -= 1
            question.save()


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

    @staticmethod
    def change_rating(answer_pk, vote):
        with transaction.atomic():
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

        Question.change_rating(question_pk=question_pk, vote=self.vote)


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

        Answer.change_rating(answer_pk=answer_pk, vote=self.vote)
