# Generated by Django 2.1 on 2018-09-07 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20180905_0927'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('coord_v', models.FloatField()),
                ('coord_h', models.FloatField()),
                ('images', models.ManyToManyField(blank=True, null=True, to='blog.Image')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=32)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='images',
            field=models.ManyToManyField(blank=True, null=True, related_name='images', to='blog.Image'),
        ),
        migrations.AlterField(
            model_name='post',
            name='instagram_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='twitter_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='place',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.PlaceStatus'),
        ),
        migrations.AddField(
            model_name='place',
            name='trip',
            field=models.ManyToManyField(blank=True, null=True, to='blog.Trip'),
        ),
        migrations.AddField(
            model_name='post',
            name='place',
            field=models.ManyToManyField(blank=True, null=True, to='blog.Place'),
        ),
    ]