# Generated by Django 4.2.6 on 2023-10-30 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0009_equipment'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='purchase_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]