import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = 'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent'


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    entities = PokemonEntity.objects.all()
    pokemons = Pokemon.objects.all()

    for entity in entities:
        pokemon = Pokemon.objects.get(id=entity.pokemon_id)
        img_url = pokemon.img_url.path

        add_pokemon(folium_map,

                    entity.lat,
                    entity.lon,

                    pokemon.title_ru,
                    img_url
                    )

    pokemons_on_page = [{'pokemon_id': pokemon.id,
                         'img_url': pokemon.img_url.url if pokemon.img_url else DEFAULT_IMAGE_URL,
                         'title_ru': pokemon.title_ru,
                         }
                        for pokemon in pokemons]

    return render(request, 'mainpage.html', context={'map': folium_map._repr_html_(),
                                                     'pokemons': pokemons_on_page, }
                  )


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)

    if not pokemon:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    entities = pokemon.entities.all()

    for entity in entities:
        add_pokemon(folium_map,

                    entity.lat,
                    entity.lon,

                    pokemon.title_ru,
                    pokemon.img_url.path
                    )

    pokemon_dict = {'title_ru': pokemon.title_ru,
                    'img_url': pokemon.img_url.url,

                    'title_en': pokemon.title_en,
                    'title_jp': pokemon.title_jp,

                    'description': pokemon.description
                    }

    if pokemon.previous_evolution:
        pokemon_dict['previous_evolution'] = {'title_ru': pokemon.previous_evolution.title_ru,
                                              'pokemon_id': pokemon.previous_evolution.id,
                                              'img_url': pokemon.previous_evolution.img_url.url
                                              }

    pokemon_next_evolutions = pokemon.next_evolutions.all()

    for pokemon_next_evolution in pokemon_next_evolutions:
        pokemon_dict['next_evolution'] = {'title_ru': pokemon_next_evolution.title_ru,
                                          'pokemon_id': pokemon_next_evolution.id,
                                          'img_url': pokemon_next_evolution.img_url.url
                                          }
        break

    return render(request, 'pokemon.html', context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_dict
                                                    }
                  )
