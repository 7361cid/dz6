from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse

from users.models import CustomUser
from .models import Question, Answer, Vote, VoteAnswer
from .forms import AskForm, QuestionForm, VoteForm, VoteAnswerForm


def question_with_answers_view(request, pk, page=1):
    question = Question.objects.get(pk=pk)
    answers = Answer.objects.filter(question_pk=pk).order_by('-rating', '-date')
    question.author.profile_avatar = CustomUser.get_avatar(question.author.pk)
    for a in answers:
        a.author.profile_avatar = CustomUser.get_avatar(a.author.pk)
    paginator = Paginator(answers, 30)
    context = {'question': question, 'answers': answers, 'paginator': paginator.page(page)}
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            answer = Answer(content=form.cleaned_data['content'], author=request.user, question_pk=pk)
            answer.save()
    else:
        form = AskForm()
    context['form'] = form
    questions_trends = Question.get_top20()
    context['questions_trends'] = questions_trends
    return render(request, 'question.html', context=context)


@login_required
def vote_for_question(request, pk):
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.user = request.user
            # If changing vote or voting virst time
            current_vote = Vote.objects.filter(question_pk=pk, user=vote.user)

            if not current_vote.exists():
                vote.set_vote(question_pk=pk)

            elif current_vote[0].vote != vote.vote:
                updating_vote = Vote.objects.get(question_pk=pk, user=vote.user)
                updating_vote.set_vote(question_pk=pk, vote=vote.vote)

    return HttpResponseRedirect(reverse('question', args=[pk]))


@login_required
def vote_for_answer(request, pk, pk2):
    if request.method == 'POST':
        form = VoteAnswerForm(request.POST)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.user = request.user
            # If changing vote or voting virst time
            current_vote = VoteAnswer.objects.filter(answer_pk=pk2, user=vote.user)

            if not current_vote.exists():
                vote.set_vote(answer_pk=pk2)

            elif current_vote[0].vote != vote.vote:
                updating_vote = VoteAnswer.objects.get(answer_pk=pk2, user=vote.user)
                updating_vote.set_vote(answer_pk=pk2, vote=vote.vote)

    return HttpResponseRedirect(reverse('question', args=[pk]))


@login_required
def make_answer_right(request, pk, pk2):
    if Question.objects.get(pk=pk).author == request.user:
        answer = Answer.objects.get(pk=pk2)
        answer.right = True
        answer.save()

    return HttpResponseRedirect(reverse('question', args=[pk]))


class QuestionCreateView(LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = 'question_new.html'
    success_url = '/'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        questions_trends = Question.get_top20()
        ctx['questions_trends'] = questions_trends
        return ctx

    def form_valid(self, form):
        form.save()

        return HttpResponseRedirect(self.success_url)
