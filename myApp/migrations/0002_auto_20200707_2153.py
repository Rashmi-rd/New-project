# Generated by Django 3.0.8 on 2020-07-07 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='Download.png', null=True, upload_to=''),
        ),
    ]
