# Generated by Django 2.2.4 on 2020-10-15 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wall_app', '0002_comment_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='message',
            new_name='content',
        ),
    ]
