# Generated by Django 3.1.2 on 2020-11-28 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0007_auto_20201120_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='bookmarked',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
