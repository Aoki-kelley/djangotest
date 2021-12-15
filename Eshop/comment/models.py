from django.db import models


class Comment(models.Model):
    goods = models.IntegerField(verbose_name='商品')  # goods.id
    title = models.CharField(verbose_name='标题', max_length=32)
    content = models.TextField(verbose_name='内容', max_length=512)
    date = models.DateTimeField(verbose_name='时间')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)


class Reply(models.Model):
    content = models.TextField(verbose_name='内容', max_length=512)
    date = models.DateTimeField(verbose_name='时间')
    from_user = models.IntegerField(verbose_name='回复人')  # user.id
    to_user = models.IntegerField(verbose_name='被回复人')  # user.id
    floor = models.IntegerField(verbose_name='楼层数')
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
