# Generated by Django 4.2.16 on 2024-10-23 10:40

import bloodbankapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodbankapp', '0006_alter_profile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='default@gmail.com', max_length=254, validators=[bloodbankapp.models.validate_gmail_email]),
        ),
    ]