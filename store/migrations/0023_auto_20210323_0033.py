# Generated by Django 3.1.7 on 2021-03-22 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_auto_20210323_0031'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sitesetting',
            old_name='no_quantity',
            new_name='show_no_quantity',
        ),
        migrations.AddField(
            model_name='sitesetting',
            name='show_quantity',
            field=models.BooleanField(default=True, verbose_name='نمایش کالاهای بدون موجودی'),
        ),
    ]
