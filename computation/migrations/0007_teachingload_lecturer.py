# Generated by Django 3.1.4 on 2021-01-28 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('computation', '0006_lecturer_lecturer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachingload',
            name='lecturer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='computation.lecturer'),
        ),
    ]
