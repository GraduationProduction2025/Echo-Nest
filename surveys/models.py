from django.db import models

# Create your models here.
# アンケートのデータベースの作成
class Survey(models.Model):
    id = models.IntegerField(primary_key = True)
    title = models.CharField(max_length = 255)
    create_at = models.DateTimeField()
    create_user = models.CharField(max_length = 255)   #users-user_idの外部キーを設定する
    published_flag = models.BooleanField(default = False, help_text = '公開済みならTrue')
    deleted_flag = models.BooleanField(default = False, help_text = '削除済みならTrue')
    def __str__(self):
        return self.title

# 選択肢形式データベース
class Choicetype(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length = 255)
    deleted_flag = models.BooleanField(default = False, help_text = '削除済みならTrue')
    def __str__(self):
        return self.type

# 質問データベース
class Question(models.Model):
    id = models.IntegerField(primary_key = True)
    title = models.CharField(max_length = 255)
    survey = models.ForeignKey(Survey, on_delete = models.CASCADE)
    type = models.ForeignKey(Choicetype, on_delete = models.CASCADE)
    deleted_flag = models.BooleanField(default = False, help_text = '削除済みならTrue')
    def __str__(self):
        return self.title

# 選択肢データベース
class Choice(models.Model):
    id = models.IntegerField(primary_key = True)
    text = models.CharField(max_length = 255)
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    deleted_flag = models.BooleanField(default = False, help_text = '削除済みならTrue')
    def __str__(self):
        return self.text
