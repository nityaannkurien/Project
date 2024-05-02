# Generated by Django 5.0.4 on 2024-05-02 03:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wish', '0004_remove_listitem_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='listitem',
            name='item_id',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='Wish.itemdetails'),
        ),
    ]
