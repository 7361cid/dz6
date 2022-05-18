from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Question, Tag, Answer


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
    context = {'question': question}
    print(f"question.author {question.author} {type(question.author)}")
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            answer = Answer(content=form.cleaned_data['content'], author=request.user, question_pk=pk)
            answer.save()
    else:
        form = AskForm()
    context['form'] = form
    return render(request, 'question.html', context=context)


class TagField(forms.Field):
    def to_python(self, value):
        """Normalize data to a Tag"""
        if not value:
            return Tag.objects.create(tag="")
        return Tag.objects.create(tag=value)

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)


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


class QuestionCreateView(LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = 'question_new.html'
    success_url = '/blog/question_list/'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        print(f"form_valid \n\n")
        form.save()

        return HttpResponseRedirect(self.success_url)
