# Generated by Django 3.0.3 on 2020-05-02 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_auto_20200501_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='name',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]