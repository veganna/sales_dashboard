# Generated by Django 4.1.1 on 2022-10-06 22:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecommerce_simple', '0006_address_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership_name', models.CharField(max_length=255)),
                ('membership_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('membership_description', models.TextField(blank=True, null=True)),
                ('membership_image', models.ImageField(blank=True, upload_to='membership')),
                ('membership_is_available', models.BooleanField(default=True)),
                ('membership_lifetime', models.CharField(default='1 month', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('membership_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
