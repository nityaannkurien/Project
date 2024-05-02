# Generated by Django 5.0.4 on 2024-05-02 03:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wish', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255, null=True)),
                ('item_id', models.CharField(default=None, max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='listitem',
            name='status',
        ),
        migrations.AddField(
            model_name='listitem',
            name='item_id',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='Wish.itemdetails'),
        ),
    ]
