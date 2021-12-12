from django.db import models


class User(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=8)
    password = models.CharField(verbose_name='密码', max_length=32)
    email = models.CharField(verbose_name='邮箱', max_length=64)
    image = models.FileField(verbose_name='头像', upload_to='user_image', default='user_image/default.png')
    money = models.FloatField(verbose_name='余额', default=0.00)
    status = models.CharField(verbose_name='状态', default='off', max_length=3)  # on/off
    email_proved = models.CharField(verbose_name='邮箱状态', default='off', max_length=3)  # on/off
    role = models.CharField(verbose_name='角色', default='', max_length=6)  # seller/buyer


class VerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=32)
    date = models.DateTimeField()
    username = models.CharField(max_length=50, default='')
