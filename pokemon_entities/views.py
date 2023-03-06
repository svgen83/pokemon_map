import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime
from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=localtime(),
        disappeared_at__gte=localtime())
    
    pokemons_on_page = []

    for pokemon_entity in pokemon_entities:
        image_url = request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            image_url
            )

    for pokemon in pokemons:
        image_url = request.build_absolute_uri(pokemon.image.url)
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url':  image_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page
        })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        raise Pokemon.DoesNotExist('Покемон не найден')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_entities = PokemonEntity.objects.get(pokemon=int(pokemon_id))
    image_url = request.build_absolute_uri(pokemon_entities.pokemon.image.url)
    add_pokemon(folium_map, pokemon_entities.latitude,
                pokemon_entities.longitude, image_url)

    pokemon_describes = {
        'pokemon_id': pokemon.id,
        'img_url': image_url,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jap': pokemon.title_jap,        
        'description': pokemon.description,
        'previous_evolution': {},
        'next_evolution': {}
        }
    
    if pokemon.previous_evolution:
        pokemon_describes['previous_evolution'] = {
            'title_ru': pokemon.previous_evolution.title,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': pokemon.previous_evolution.image.url,
        }
  
    if pokemon.next_evolutions.first():
        pokemon_describes['next_evolution'] = {
            'pokemon_id': pokemon.next_evolutions.first().id,
            'title_ru': pokemon.next_evolutions.first().title,
            'img_url': pokemon.next_evolutions.first().image.url,
        }

    return render(request, 'pokemon.html', context={
                      'map': folium_map._repr_html_(),
                      'pokemon': pokemon_describes}
                  )
