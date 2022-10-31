# Generated by Django 2.2.16 on 2022-10-29 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20221029_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='genre',
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(null=True, related_name='genre', to='reviews.Genre', verbose_name='Произведение'),
        ),
    ]