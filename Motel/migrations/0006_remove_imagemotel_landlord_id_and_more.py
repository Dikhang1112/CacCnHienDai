# Generated by Django 5.1.5 on 2025-02-02 15:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Motel', '0005_remove_imagemotel_url_imagemotel_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagemotel',
            name='landlord_id',
        ),
        migrations.AddField(
            model_name='imagemotel',
            name='post_landlord',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='Motel.post_landlord'),
        ),
    ]
