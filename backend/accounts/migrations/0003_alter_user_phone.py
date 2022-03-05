# Generated by Django 4.0.1 on 2022-03-05 20:49

import accounts.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_remove_user_otp_remove_user_otp_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.CharField(
                max_length=11, unique=True, validators=[accounts.utils.phone_validator]
            ),
        ),
    ]