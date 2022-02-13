# Generated by Django 4.0 on 2022-02-11 11:37

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('brevet_database', '0001_initial'),
        ('users', '0003_alter_user_managers_remove_user_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='user',
            name='randonneur',
            field=models.OneToOneField(default=239, on_delete=django.db.models.deletion.PROTECT, to='brevet_database.randonneur'),
        ),
    ]