# Generated by Django 3.2.6 on 2021-10-03 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_alter_productvariation_stock'),
        ('cart', '0011_auto_20211003_2059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='productvariation',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='productvariation',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='store.productvariation'),
            preserve_default=False,
        ),
    ]
