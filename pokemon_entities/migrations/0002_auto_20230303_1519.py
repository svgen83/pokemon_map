# Generated by Django 3.1.14 on 2023-03-03 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='title_en',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='title_jap',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
