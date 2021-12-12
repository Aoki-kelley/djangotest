from django.db import models
from user.models import User
from tinymce.models import HTMLField


class Goods(models.Model):
    image = models.FileField(verbose_name='图像', upload_to='goods_image', default='default.png')
    title = models.CharField(verbose_name='商品名', max_length=16)
    detail = HTMLField(verbose_name='描述', max_length=512)
    label = models.CharField(verbose_name='标签', max_length=32)
    seller = models.ForeignKey('user.User', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='创建时间')
    price = models.FloatField(verbose_name='单价')
    amount = models.IntegerField(verbose_name='余量')
    status = models.CharField(verbose_name='状态', default='off', max_length=3)  # on/off


class Order(models.Model):
    goods = models.IntegerField(verbose_name='商品')  # goods.id
    title = models.CharField(verbose_name='商品名', max_length=16)
    seller = models.IntegerField(verbose_name='卖家')  # user.id
    buyer = models.IntegerField(verbose_name='买家')  # user.id
    date = models.DateTimeField(verbose_name='创建时间')
    amount = models.IntegerField(verbose_name='数量')
    price = models.FloatField(verbose_name='单价')
    status = models.CharField(verbose_name='状态', default='not_deal', max_length=8)  # on/off/not_deal


class Wish(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    goods = models.IntegerField(verbose_name='商品')  # goods.id
    seller = models.IntegerField(verbose_name='卖家')  # user.id
    date = models.DateTimeField(verbose_name='收藏时间')
