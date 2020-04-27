# Generated by Django 3.0.5 on 2020-04-25 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0028_auto_20200423_0323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noteobject',
            name='pitch',
            field=models.IntegerField(choices=[(1, 'C3'), (2, 'D3'), (3, 'E3'), (4, 'F3'), (5, 'G3'), (6, 'A3'), (7, 'B3'), (8, 'C4'), (9, 'D4'), (10, 'E4'), (11, 'F4'), (12, 'G4'), (13, 'A4'), (14, 'B4'), (15, 'C5'), (16, 'D5'), (17, 'E5'), (18, 'F5'), (19, 'G5'), (20, 'A5'), (21, 'B5'), (22, 'C6')], default=8),
        ),
    ]
