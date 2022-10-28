# Generated by Django 4.0.5 on 2022-08-29 17:58

from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_message_sender_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sender_id',
            field=models.OneToOneField(choices=[(users.models.Developer, 'Developer'), (users.models.Business, 'Business')], on_delete=django.db.models.deletion.CASCADE, to='users.developer'),
        ),
    ]