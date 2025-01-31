# Generated by Django 3.1.14 on 2023-03-06 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('title_en', models.CharField(blank=True, max_length=200, null=True)),
                ('title_jap', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('description', models.TextField(blank=True, default='', max_length=2000)),
                ('previous_evolution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_evolutions', to='pokemon_entities.pokemon')),
            ],
        ),
        migrations.CreateModel(
            name='PokemonEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('appeared_at', models.DateTimeField(blank=True, null=True)),
                ('disappeared_at', models.DateTimeField(blank=True, null=True)),
                ('level', models.IntegerField(default=0)),
                ('health', models.IntegerField(default=0)),
                ('strength', models.IntegerField(default=0)),
                ('defence', models.IntegerField(default=0)),
                ('stamina', models.IntegerField(default=0)),
                ('pokemon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pokemon_entities.pokemon')),
            ],
        ),
    ]
