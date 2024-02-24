# Generated by Django 5.0.2 on 2024-02-23 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_address_person_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='address',
        ),
        migrations.AddField(
            model_name='person',
            name='address',
            field=models.ManyToManyField(null=True, related_name='add', to='api.address'),
        ),
    ]
