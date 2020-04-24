# Generated by Django 3.0.2 on 2020-03-10 05:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import generator.models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0017_auto_20200310_0507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='user',
            field=models.ForeignKey(default=generator.models.CustomUser, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
