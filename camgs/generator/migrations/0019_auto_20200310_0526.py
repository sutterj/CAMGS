# Generated by Django 3.0.2 on 2020-03-10 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0018_auto_20200310_0518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
