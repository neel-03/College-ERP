# Generated by Django 5.1.4 on 2025-03-15 11:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_course_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='course', to='main_app.admin'),
        ),
    ]
