# Generated by Django 3.2.9 on 2021-11-15 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TakeOutSystem', '0002_alter_order_payment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='r_delivery_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee3', to='TakeOutSystem.employee'),
        ),
    ]
