# Generated by Django 3.2.6 on 2021-10-05 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_alter_vendor_due_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='due_payment',
            field=models.FloatField(default=0),
        ),
    ]