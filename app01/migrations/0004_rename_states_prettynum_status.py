# Generated by Django 4.2 on 2023-04-25 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_prettynum'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prettynum',
            old_name='states',
            new_name='status',
        ),
    ]