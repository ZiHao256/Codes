# Generated by Django 3.2.9 on 2021-11-16 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TakeOutSystem', '0007_remove_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
