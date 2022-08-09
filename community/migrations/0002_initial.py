# Generated by Django 4.0.6 on 2022-08-09 05:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0001_initial'),
        ('park', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlecomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자'),
        ),
        migrations.AddField(
            model_name='article',
            name='park',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='park.park', verbose_name='공원 이름'),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.tag', verbose_name='태그'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자'),
        ),
    ]
