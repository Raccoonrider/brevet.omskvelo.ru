# Generated by Django 4.0 on 2022-09-08 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brevet_database', '0011_application_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
