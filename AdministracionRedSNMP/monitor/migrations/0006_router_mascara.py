# Generated by Django 2.1.7 on 2019-05-29 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0005_auto_20190529_0036'),
    ]

    operations = [
        migrations.AddField(
            model_name='router',
            name='mascara',
            field=models.PositiveSmallIntegerField(default=24),
            preserve_default=False,
        ),
    ]
