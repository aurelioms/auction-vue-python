# Generated by Django 3.2.5 on 2022-12-10 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctioning', '0002_auto_20221209_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='newusername',
            field=models.CharField(default='new', max_length=50),
        ),
    ]
