# Generated by Django 4.1.3 on 2022-11-25 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postit_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-created_at',)},
        ),
    ]
