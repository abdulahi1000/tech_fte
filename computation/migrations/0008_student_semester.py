# Generated by Django 3.0.6 on 2020-12-30 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computation', '0007_auto_20201218_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='semester',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
