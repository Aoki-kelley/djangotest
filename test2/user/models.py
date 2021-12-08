from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default='NONE')
    anonymity = models.CharField(max_length=50)  # 匿名


# 邮箱验证码
class VerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=32)
    date = models.DateTimeField()
    username = models.CharField(max_length=50, default='')
