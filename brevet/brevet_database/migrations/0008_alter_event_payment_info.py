# Generated by Django 4.0 on 2022-05-23 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brevet_database', '0007_paymentinfo_event_payment_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='payment_info',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='brevet_database.paymentinfo'),
        ),
    ]
