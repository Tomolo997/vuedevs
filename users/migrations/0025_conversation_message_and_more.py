# Generated by Django 4.0.5 on 2022-08-30 15:55

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_alter_messagebusinesstodeveloper_receipter_id_developer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('business_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.business')),
                ('developer_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.developer')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('sender_id', models.UUIDField()),
                ('sender_type', models.CharField(blank=True, max_length=200, null=True)),
                ('body', models.TextField()),
                ('is_read', models.BooleanField(default=False, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('conversation', models.ManyToManyField(blank=True, to='users.conversation')),
            ],
            options={
                'ordering': ['is_read', '-created'],
            },
        ),
        migrations.DeleteModel(
            name='MessageBusinessToDeveloper',
        ),
    ]