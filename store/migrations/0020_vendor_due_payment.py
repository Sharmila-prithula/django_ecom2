# Generated by Django 3.2.6 on 2021-10-05 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_alter_productvariation_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='due_payment',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]