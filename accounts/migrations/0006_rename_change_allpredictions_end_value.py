# Generated by Django 5.0.9 on 2025-01-02 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_customuser_accuracy_allpredictions_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allpredictions',
            old_name='change',
            new_name='end_value',
        ),
    ]
