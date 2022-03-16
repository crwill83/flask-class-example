from flask import Blueprint, redirect, render_template, request, url_for
import requests as r

pokemon = Blueprint('pokemon', __name__, template_folder="pokemon_templates")

from app.models import db, Pokemon

@pokemon.route('/my-pokemon')
def showPokedex():
    pokedex = Pokemon.query.all()[::-1]
    return render_template('my-pokemon.html', pokedex=pokedex)

@pokemon.route('/pokedex', methods=["GET", "POST"])
def addToPokedex():
    name = request.form.to_dict()['name']
    data = r.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    my_data = data.json()
    abilities = my_data['abilities']
    my_abilities = []

    
    for item in abilities:
        my_abilities.append(item['ability']['name'])
    print(my_abilities)

    poke_name = name
    image = my_data['sprites']['front_default']
    ability1 = my_abilities[0]
    ability2 = my_abilities[1]


    pokemon = Pokemon(poke_name, image, ability1, ability2)

    # check for pokemon already in database and only adds new pokemon
    if Pokemon.query.filter_by(name=poke_name).first():
        print('Pokemon already exists.')
    else:
        db.session.add(pokemon)
        db.session.commit()

    return redirect(url_for('pokemon.showPokedex'))


@pokemon.route('/pokemon', methods=["POST"])
def myPokemon():
    name = request.form.to_dict()['name']
    data = r.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    if data.status_code == 200:
        my_data = data.json()
        abilities = my_data['abilities']
        my_abilities = []
        for item in abilities:
            my_abilities.append((item['ability']['name']))
        my_img = my_data['sprites']['front_default']
        return render_template('pokemon.html', abilities=my_abilities, img_url=my_img, name=name)
    return redirect(url_for('home'))