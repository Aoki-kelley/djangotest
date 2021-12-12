import datetime
import uuid

from django.core.mail import send_mail
from django.conf import settings

from celery import Task

from user.models import VerificationCode


class SendEmailTask(Task):
    def run(self, email, username, label='register'):
        code = str(uuid.uuid1())[0:5].upper()
        target = VerificationCode.objects.filter(username__exact=username)
        if target:
            target.delete()
        VerificationCode.objects.create(email=email, code=code,
                                        date=datetime.datetime.now(), username=username)
        if label == 'register':
            subject = '邮箱验证'
            message = '尊敬的{username},你的验证码为{code}，请在五分钟内进行验证。\n请不要回复该邮件。'.format(username=username, code=code)
            sender = settings.EMAIL_FROM
            receiver = [email]
            send_mail(subject, message, sender, receiver)
        elif label == 'reset_password':
            subject = '更改密码'
            message = '尊敬的{username},你的验证码为{code}，请在五分钟内进行验证。' \
                      '\n请不要回复该邮件，不要将验证码告诉他人。'.format(username=username, code=code)
            sender = settings.EMAIL_FROM
            receiver = [email]
            send_mail(subject, message, sender, receiver)
