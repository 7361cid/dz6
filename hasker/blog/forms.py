from django import forms

from .models import Question, Tag, Answer, Vote, VoteAnswer
from .fields import TagField


class AskForm(forms.ModelForm):
    content = forms.CharField(max_length=10000)

    class Meta:
        model = Answer
        fields = ["content"]


class QuestionForm(forms.ModelForm):
    tag = TagField()
    title = forms.CharField(max_length=255)
    content = forms.CharField(max_length=10000)

    class Meta:
        model = Question
        fields = ["title", "content", "tag"]

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(QuestionForm, self).__init__(*args, **kwargs)
        tag_objects = Tag.objects.all()
        if len(tag_objects) >= 2:
            example = f"Tags examples: {str(tag_objects[0])}, {str(tag_objects[1])} "
            self.fields['tag'].widget.attrs['placeholder'] = example
        else:
            self.fields['tag'].widget.attrs['placeholder'] = 'No tags created yet'

    def save(self):
        data = self.cleaned_data
        question = Question(title=data['title'], content=data['content'], author=self.user)
        question.save()
        if 'tag' in data.keys():
            tags = str(data['tag']).split(',')
            for tag in tags:
                question.tags.create(tag=tag)
                question.save()


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['vote']
        widgets = {'vote': forms.HiddenInput()}


class VoteAnswerForm(forms.ModelForm):
    class Meta:
        model = VoteAnswer
        fields = ['vote']
        widgets = {'vote': forms.HiddenInput()}