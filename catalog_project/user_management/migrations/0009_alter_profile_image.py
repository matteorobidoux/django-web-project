# Generated by Django 4.0.4 on 2022-05-16 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0008_alter_profile_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_pics/default-user.png', upload_to='profile_pics'),
        ),
    ]
