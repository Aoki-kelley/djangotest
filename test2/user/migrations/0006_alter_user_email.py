# Generated by Django 3.2.8 on 2021-10-30 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_user_anonymity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(default='NONE', max_length=50),
        ),
    ]
