# Generated by Django 4.0.3 on 2022-05-01 01:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item_catalog', '0014_alter_rating_rate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='rate',
            new_name='rating',
        ),
    ]
