# Generated by Django 3.0.3 on 2020-04-30 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='subject',
            field=models.CharField(max_length=50),
        ),
    ]
