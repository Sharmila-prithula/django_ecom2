# Generated by Django 3.2.6 on 2021-09-27 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_auto_20210926_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariation',
            name='stock',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]