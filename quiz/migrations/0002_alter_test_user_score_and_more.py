# Generated by Django 4.0.5 on 2022-06-26 19:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test_user',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='test_user',
            unique_together={('user', 'test_event')},
        ),
    ]
