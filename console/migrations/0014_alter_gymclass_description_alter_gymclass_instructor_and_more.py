# Generated by Django 4.2.6 on 2023-11-07 00:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('console', '0013_delete_trainer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gymclass',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gymclass',
            name='instructor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='gymclass',
            name='max_capacity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gymclass',
            name='schedule',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
