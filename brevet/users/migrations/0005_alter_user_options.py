# Generated by Django 4.0 on 2023-07-09 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_oauth'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]