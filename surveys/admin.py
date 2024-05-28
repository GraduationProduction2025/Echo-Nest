from django.contrib import admin
# アンケートDBの読み取り
from .models import Survey,Question,Choice,Choicetype

# Register your models here.
# adminサイトでアンケートのデータベースを見る
class SurveysAdmin(admin.ModelAdmin):
    list_display = ('Survey', 'Question', 'Choice', 'Choicetype')

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Choicetype)