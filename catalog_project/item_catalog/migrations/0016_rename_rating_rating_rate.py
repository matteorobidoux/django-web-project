# Generated by Django 4.0.3 on 2022-05-01 01:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item_catalog', '0015_rename_rate_rating_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='rating',
            new_name='rate',
        ),
    ]
