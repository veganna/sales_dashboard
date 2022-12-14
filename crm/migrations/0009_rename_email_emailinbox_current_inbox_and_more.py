# Generated by Django 4.1.1 on 2022-10-18 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_emailinbox_remove_tasks_notes_alter_notes_action_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailinbox',
            old_name='email',
            new_name='current_inbox',
        ),
        migrations.AddField(
            model_name='emailinbox',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
