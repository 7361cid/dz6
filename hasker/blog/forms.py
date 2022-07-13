from django import forms

from .models import Question, Tag, Answer, Vote, VoteAnswer


class AskForm(forms.ModelForm):
    content = forms.CharField(max_length=10000)

    class Meta:
        model = Answer
        fields = ["content"]


class TagField(forms.Field):
    def to_python(self, value):
        if not value:
            return Tag.objects.create(tag="")
        return Tag.objects.create(tag=value)

    def validate(self, value):
        tags_list = str(value).split(',')
        if len(tags_list) > 3:
            raise forms.ValidationError("You can't use more than 3 tags")
        tags_list2 = list(set(tags_list))
        if sorted(tags_list) != sorted(tags_list2):
            raise forms.ValidationError("You use equal tags")


class QuestionForm(forms.ModelForm):
    tag = TagField()
    title = forms.CharField(max_length=255)
    content = forms.CharField(max_length=10000)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(QuestionForm, self).__init__(*args, **kwargs)
        tag_objects = Tag.objects.all()
        if len(tag_objects) >= 2:
            example = f"Tags examples: {str(tag_objects[0])}, {str(tag_objects[1])} "
            self.fields['tag'].widget.attrs['placeholder'] = example
        else:
            self.fields['tag'].widget.attrs['placeholder'] = 'No tags created yet'

    class Meta:
        model = Question
        fields = ["title", "content", "tag"]

    def save(self):
        data = self.cleaned_data
        tags = str(data['tag']).split(',')
        if len(tags) == 1:
            question = Question(title=data['title'], content=data['content'],
                                tag=data['tag'], author=self.user)
        elif len(tags) == 2:
            tag2 = Tag.objects.create(tag=tags[1])
            question = Question(title=data['title'], content=data['content'],
                                tag=data['tag'], tag2=tag2, author=self.user)
        else:
            tag2 = Tag.objects.create(tag=tags[1])
            tag3 = Tag.objects.create(tag=tags[1])
            question = Question(title=data['title'], content=data['content'],
                                tag=data['tag'], tag2=tag2, tag3=tag3, author=self.user)
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