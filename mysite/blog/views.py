from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django import forms
from django.http import HttpResponseRedirect

from .models import Question, Tag


class QuestionListView(ListView):
    model = Question
    template_name = 'question_list.html'


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'question.html'


class TagField(forms.Field):
    def to_python(self, value):
        """Normalize data to a Tag"""
        # Return an empty list if no input was given.
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
        print(f"INIT? \n\n")
     #   self.save()

    class Meta:
        model = Question
        fields = ["title", "content", "tag"]

    def save(self):
        print(f"self {dir(self)} \n\n")
        data = self.cleaned_data
        question = Question(title=data['title'], content=data['content'],  # Create?
                            tag=data['tag'], author=self.user)
        print(f"Questions2 {Question.objects.all()}\n\n")
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
