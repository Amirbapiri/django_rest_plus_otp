# Generated by Django 4.0.1 on 2022-03-05 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("otp", "0002_otp_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="otp",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
