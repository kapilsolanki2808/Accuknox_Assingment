# Generated by Django 5.0.3 on 2024-04-03 13:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='friend_of', to=settings.AUTH_USER_MODEL)),
                ('you', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='friends', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
