# Generated by Django 4.0.3 on 2022-10-12 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_posts_creationtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='Thumbnail',
            field=models.FileField(null=True, upload_to='./thumbnail'),
        ),
    ]
