# Generated by Django 4.0.3 on 2023-07-24 19:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EMG_signal_date',
            new_name='EMG_user_data',
        ),
        migrations.RenameModel(
            old_name='EMG_signal',
            new_name='EMG_value',
        ),
    ]
