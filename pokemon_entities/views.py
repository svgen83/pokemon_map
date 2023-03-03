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
        pokemon = Pokemon.objects.get(id=int(pokemon_id))
    except Pokemon.DoesNotExist:
        raise Pokemon.DoesNotExist('Покемон не найден')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_entity = PokemonEntity.objects.get(pokemon=int(pokemon_id))
    image_url = request.build_absolute_uri(pokemon_entity.pokemon.image.url)
    add_pokemon(folium_map, pokemon_entity.latitude,
                pokemon_entity.longitude, image_url)

    pokemon_descr = {
        'img_url': image_url,
        'title_ru': pokemon.title,
        'description': pokemon.description
        }

    return render(request, 'pokemon.html', context={
                      'map': folium_map._repr_html_(),
                      'pokemon': pokemon_descr}
                  )
