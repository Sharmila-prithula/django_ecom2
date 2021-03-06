# Generated by Django 3.2.6 on 2021-09-26 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_auto_20210926_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariation',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='stock',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
