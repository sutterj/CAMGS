# Generated by Django 3.0.4 on 2020-03-10 05:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0020_auto_20200310_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]