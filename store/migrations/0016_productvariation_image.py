# Generated by Django 3.2.6 on 2021-09-26 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_productvariation_variants'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariation',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]