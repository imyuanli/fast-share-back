from django.db import models


class Login(models.Model):
    # Create your models here.
    email = models.CharField("邮箱", max_length=32)
    login_code = models.CharField("验证码", max_length=32)
    user_token = models.CharField(max_length=50)

    class Meta:
        db_table = 'table_login'  # 重命名


class User(models.Model):
    user_id = models.AutoField("id", primary_key=True)
    user_token = models.CharField(max_length=50)
    user_email = models.CharField(max_length=32)
    user_name = models.CharField(max_length=255, unique=True)
    user_avatar = models.CharField(max_length=255)
    user_collection = models.CharField(max_length=255, default=-1)

    class Meta:
        db_table = 'table_user'  # 重命名
