from django import forms

from .models import Tag


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