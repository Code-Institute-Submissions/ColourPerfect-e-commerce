# Generated by Django 3.0.6 on 2020-06-07 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20200607_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colour',
            name='name',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
