# Generated by Django 3.2.6 on 2021-09-13 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_verification_token',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='forget_password_token',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]