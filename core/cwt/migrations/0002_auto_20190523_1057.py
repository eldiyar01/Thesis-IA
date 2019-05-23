# Generated by Django 2.2 on 2019-05-23 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cwt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userresult',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_results', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='useranswer',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='cwt.Answer'),
        ),
        migrations.AddField(
            model_name='useranswer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='variants',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='cwt.Variant'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='cwt.Question'),
        ),
    ]