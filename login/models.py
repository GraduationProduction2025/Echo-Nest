from django.db import models

# Create your models here.
# ユーザのデータベースの作成
class Users(models.Model):
    user_id = models.IntegerField(primary_key = True)
    user_name = models.CharField(max_length = 100)
    user_pass = models.CharField(max_length = 100)
    user_pass_v = models.CharField(max_length = 100)

# 管理者のデータベースの作成
class Admins(models.Model):
    admin_id = models.IntegerField(primary_key = True)
    admin_name = models.CharField(max_length = 100)
    admin_pass = models.CharField(max_length = 100)
    admin_pass_v = models.CharField(max_length = 100)