# Generated by Django 4.1.1 on 2022-10-06 23:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecommerce_simple', '0008_remove_membership_membership_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='membership_user',
        ),
        migrations.AddField(
            model_name='membership',
            name='membership_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]