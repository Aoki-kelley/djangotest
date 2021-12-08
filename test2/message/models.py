from django.db import models


# Create your models here.
class Message(models.Model):
    username = models.CharField(max_length=32)
    anonymity = models.CharField(max_length=50, default='')
    title = models.CharField(max_length=32)
    content = models.TextField(max_length=256)
    date = models.DateTimeField()

    def __str__(self):
        tpl = '<Message:[username={username},title={title}, content={content}, date={date}]>'
        return tpl.format(username=self.username, title=self.title,
                          content=self.content, date=self.date)


class Reply(models.Model):
    mid = models.ForeignKey('Message', on_delete=models.CASCADE)  #mid_id
    username = models.CharField(max_length=32)
    anonymity = models.CharField(max_length=50, default='')
    content = models.TextField(max_length=256)
    date = models.DateTimeField()

    def __str__(self):
        tpl = '<Reply:[username={username}, content={content}, date={date}]>'
        return tpl.format(username=self.username, content=self.content, date=self.date)
