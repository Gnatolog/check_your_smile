# Generated by Django 5.0.3 on 2024-03-28 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostic', '0012_alter_photodiagnostic_image_frontal_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alldiagnostic',
            name='slug',
        ),
    ]