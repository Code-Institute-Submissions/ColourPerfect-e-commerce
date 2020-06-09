# Generated by Django 3.0.6 on 2020-06-09 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20200609_0956'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, null=True)),
                ('display_name', models.CharField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ManyToManyField(to='products.Brand'),
        ),
    ]
