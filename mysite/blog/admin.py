from django.contrib import admin
from .models import Question, Tag, Answer, Vote

admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(Vote)
