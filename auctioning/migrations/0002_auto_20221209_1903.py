# Generated by Django 3.2.5 on 2022-12-09 19:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctioning', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='questions',
            field=models.ManyToManyField(blank=True, related_name='related_to', through='auctioning.Question', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent', to='auctioning.product'),
        ),
    ]