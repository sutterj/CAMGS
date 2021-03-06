# Generated by Django 3.0.4 on 2020-03-10 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0025_auto_20200310_0551'),
    ]

    operations = [
        migrations.AddField(
            model_name='noteobject',
            name='accidental',
            field=models.CharField(choices=[('double-flat', 'double-flat'), ('flat', 'flat'), ('natural', 'natural'), ('sharp', 'sharp'), ('double-sharp', 'double-sharp'), ('', 'none')], default='', max_length=12),
        ),
        migrations.AddField(
            model_name='noteobject',
            name='octave',
            field=models.IntegerField(choices=[(3, '3'), (4, '4'), (5, '5'), (6, '6')], default='4'),
        ),
        migrations.AddField(
            model_name='noteobject',
            name='pitch',
            field=models.CharField(choices=[('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('A', 'A'), ('B', 'B')], default='C', max_length=1),
        ),
    ]
