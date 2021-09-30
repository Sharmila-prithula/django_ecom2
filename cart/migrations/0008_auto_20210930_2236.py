# Generated by Django 3.2.6 on 2021-09-30 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_auto_20210930_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_item',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cartitem', to='cart.cart'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='order', to='cart.cart'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='orderitem', to='cart.order'),
        ),
    ]