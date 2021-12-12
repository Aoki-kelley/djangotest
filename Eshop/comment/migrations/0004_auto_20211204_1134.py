# Generated by Django 3.2.8 on 2021-12-04 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='title',
            field=models.CharField(default='', max_length=32, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(verbose_name='时间'),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=512, verbose_name='内容')),
                ('date', models.DateTimeField(verbose_name='时间')),
                ('from_user', models.CharField(max_length=8, verbose_name='回复人')),
                ('to_user', models.CharField(max_length=8, verbose_name='被回复人')),
                ('floor', models.IntegerField(verbose_name='楼层数')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comment.comment')),
            ],
        ),
    ]
