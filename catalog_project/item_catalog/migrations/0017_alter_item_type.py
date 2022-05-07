# Generated by Django 4.0.4 on 2022-05-07 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item_catalog', '0016_rename_rating_rating_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(choices=[('Practical', 'PRACTICAL'), ('Theoretical', 'THEORETICAL'), ('Fundamental research', 'FUNDAMENTAL RESEARCH'), ('Empirical', 'Empirical')], default='practical', max_length=30),
        ),
    ]
