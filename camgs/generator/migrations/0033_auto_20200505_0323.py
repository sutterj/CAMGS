# Generated by Django 3.0.5 on 2020-05-05 03:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0032_auto_20200504_1846'),
    ]

    operations = [
        migrations.RenameField(
            model_name='composition',
            old_name='base_duration',
            new_name='base_beat',
        ),
        migrations.RenameField(
            model_name='composition',
            old_name='bar_beat',
            new_name='beats_per_bar',
        ),
    ]