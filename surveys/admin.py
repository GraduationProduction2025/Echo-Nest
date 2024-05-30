from django.contrib import admin
from surveys.models import Survey, Question, Choice, Choicetype

# Register your models here.
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Choicetype)
