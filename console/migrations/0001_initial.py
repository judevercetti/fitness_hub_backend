# Generated by Django 4.2.6 on 2023-10-12 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('memberID', models.CharField(max_length=50)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('dateOfBirth', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('contactNumber', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=200)),
                ('joinDate', models.DateField()),
                ('membershipExpiryDate', models.DateField()),
                ('membershipPlan', models.CharField(max_length=50)),
            ],
        ),
    ]