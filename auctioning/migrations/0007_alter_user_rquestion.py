# Generated by Django 3.2.5 on 2022-12-14 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctioning', '0006_rename_question_user_rquestion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='rquestion',
            field=models.ManyToManyField(blank=True, related_name='related_to', to='auctioning.Rquestion'),
        ),
         migrations.AddField(
            model_name='user',
            name='rquestion',
            field=models.ManyToManyField(blank=True, related_name='related_to', to='auctioning.Rquestion'),
        ),
    ]
