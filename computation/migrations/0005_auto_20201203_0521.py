# Generated by Django 3.0.6 on 2020-12-03 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computation', '0004_fte_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fte',
            name='fte',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
        ),
    ]
