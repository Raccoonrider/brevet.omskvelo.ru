# Generated by Django 4.0 on 2021-12-17 05:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brevet_database', '0021_alter_randonneur_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ['-event__date']},
        ),
        migrations.AlterModelOptions(
            name='route',
            options={'ordering': ['slug']},
        ),
    ]
