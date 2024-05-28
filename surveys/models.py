from django.db import models

# Create your models here.
# アンケートのデータベースの作成
class Survey(models.Model):
    id = models.IntegerField(primary_key = True)
    title = models.CharField(max_length = 255)
    url = models.URLField()
    created_at = models.DateTimeField()
    create_user = models.CharField(max_length = 255)   #users-user_idの外部キーを設定する
    deleted_flag = models.BooleanField(default = False, help_text = '削除済みならTrue')

# 選択肢形式データベース
class Choicetype(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length = 255)

# 質問データベース
class Question(models.Model):
    id = models.IntegerField(primary_key = True)
    title = models.CharField(max_length = 255)
    survey_id = models.ForeignKey(Survey, on_delete = models.CASCADE)
    type_id = models.ForeignKey(Choicetype, on_delete = models.CASCADE)

# 選択肢データベース
class Choice(models.Model):
    id = models.IntegerField(primary_key = True)
    text = models.CharField(max_length = 255)
    question_id = models.ForeignKey(Question, on_delete = models.CASCADE)
