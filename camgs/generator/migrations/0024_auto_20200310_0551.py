# Generated by Django 3.0.4 on 2020-03-10 05:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0023_auto_20200310_0548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='noteobject',
            name='composition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generator.Composition'),
        ),
    ]
