# Generated by Django 3.2.6 on 2021-09-23 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_attributevalue_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='variants',
            field=models.ManyToManyField(related_name='product', to='store.Variant'),
        ),
    ]
