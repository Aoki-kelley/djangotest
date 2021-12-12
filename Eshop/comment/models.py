from django.db import models


class Comment(models.Model):
    title = models.CharField(verbose_name='标题', max_length=32)
    content = models.TextField(verbose_name='内容', max_length=512)
    date = models.DateTimeField(verbose_name='时间')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)


class Reply(models.Model):
    content = models.TextField(verbose_name='内容', max_length=512)
    date = models.DateTimeField(verbose_name='时间')
    from_user = models.CharField(verbose_name='回复人', max_length=8)
    to_user = models.CharField(verbose_name='被回复人', max_length=8)
    floor = models.IntegerField(verbose_name='楼层数')
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
