# Generated by Django 4.0.3 on 2023-07-29 08:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_remove_emg_value_author_delete_emg_user_data_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EMG_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_date', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='value',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EMG_value', models.FloatField()),
                ('author_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.emg_data')),
            ],
        ),
    ]
