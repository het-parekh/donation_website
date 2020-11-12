# Generated by Django 3.1.2 on 2020-11-11 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0008_auto_20201111_0221'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='note',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='terms_accepted',
            field=models.BooleanField(default=False, verbose_name='I agree to the Terms and Conditions*'),
        ),
    ]
