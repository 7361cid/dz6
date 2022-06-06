from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Question, Tag, Answer, Vote


class QuestionListView(ListView):
    model = Question
    template_name = 'question_list.html'


class AskForm(forms.ModelForm):
    content = forms.CharField(max_length=10000)

    class Meta:
        model = Answer
        fields = ["content"]


def question_with_answers_view(request, pk):
    question = Question.objects.get(pk=pk)
    answers = Answer.objects.filter(question_pk=pk)
    context = {'question': question, 'answers': answers}
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            answer = Answer(content=form.cleaned_data['content'], author=request.user, question_pk=pk)
            answer.save()
    else:
        form = AskForm()
    context['form'] = form
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
            print(f"LOG {current_vote} ")

            if not current_vote.exists():
                vote.set_vote(question_pk=pk)

            elif current_vote[0].vote != vote.vote:
                updating_vote = Vote.objects.get(question_pk=pk, user=vote.user)
                updating_vote.set_vote(question_pk=pk, vote=vote.vote)

    return redirect(f'/blog/question_list/{pk}')


class TagField(forms.Field):
    def to_python(self, value):
        """Normalize data to a Tag"""
        if not value:
            return Tag.objects.create(tag="")
        return Tag.objects.create(tag=value)

    def validate(self, value):
        super().validate(value)
        if len(str(value).split(',')) > 3:
            raise forms.ValidationError("You can't use more than 3 tags")


class QuestionForm(forms.ModelForm):
    tag = TagField()
    title = forms.CharField(max_length=255)
    content = forms.CharField(max_length=10000)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(QuestionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ["title", "content", "tag"]

    def save(self):
        data = self.cleaned_data
        question = Question(title=data['title'], content=data['content'],
                            tag=data['tag'], author=self.user)
        question.save()


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['vote']   # ['vote', 'question']
        widgets = {'vote': forms.HiddenInput()}


class QuestionCreateView(LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = 'question_new.html'
    success_url = '/blog/question_list/'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()

        return HttpResponseRedirect(self.success_url)
