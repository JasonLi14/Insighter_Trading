# Generated by Django 5.0.9 on 2025-01-01 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_allpredictions'),
    ]

    operations = [
        migrations.DeleteModel(
            name='allPredictions',
        ),
    ]