# Generated by Django 3.2.6 on 2021-10-03 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_alter_productvariation_stock'),
        ('cart', '0008_auto_20210930_2236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='productvariation',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='productvariation',
            field=models.ManyToManyField(to='store.ProductVariation'),
        ),
    ]
