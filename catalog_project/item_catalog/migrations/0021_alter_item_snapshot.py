# Generated by Django 4.0.4 on 2022-05-14 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item_catalog', '0020_merge_20220508_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='snapshot',
            field=models.ImageField(default='project_photos/default.jpg', upload_to='project_photos'),
        ),
    ]
