# Generated by Django 3.1.7 on 2021-03-17 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20210318_0319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=200, null=True, unique=True),
        ),
    ]