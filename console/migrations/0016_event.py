# Generated by Django 4.2.6 on 2023-11-15 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0015_alter_userprofile_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('is_all_day', models.BooleanField(default=False)),
                ('is_recurring', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]