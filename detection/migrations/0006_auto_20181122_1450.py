# Generated by Django 2.1.2 on 2018-11-22 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0005_log_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='path',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
