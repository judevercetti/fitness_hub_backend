# Generated by Django 4.2.6 on 2023-10-17 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0005_alter_member_join_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='membership_expiry_date',
        ),
    ]