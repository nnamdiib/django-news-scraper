# Generated by Django 2.0.1 on 2018-01-19 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0006_auto_20180119_0400'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='keywords',
            field=models.CharField(default='None', max_length=250),
            preserve_default=False,
        ),
    ]