# Generated by Django 2.1.1 on 2019-01-23 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20190123_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='images', to='blog.Image'),
        ),
    ]