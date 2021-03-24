from flask import Flask, render_template, url_for, request
import sqlalc
import requests
import json
app = Flask(__name__)

baseUrl = 'https://pokeapi.co/api/v2/'
typeDictionary = {
    'normal': 1,
    'fighting': 2,
    'flying': 3,
    'poison': 4,
    'ground': 5,
    'rock': 6,
    'bug': 7,
    'ghost': 8,
    'steel': 9,
    'fire': 10,
    'water': 11,
    'grass': 12,
    'electric': 13,
    'psychic': 14,
    'ice': 15,
    'dragon': 16,
    'dark': 17,
    'fairy': 18,
    'unknown': 10001,
    'shadow': 10002}
data = []

#TODO: Create a session
#TODO: Organize files with blueprint

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/team', methods=['GET', 'POST'])
def team():
    search = None
    displayNotFound = False
    pokemon = None
    if request.method == "GET":
        search = request.args.get("search")
        res = requests.get(baseUrl + f'pokemon/{search}')
        print(baseUrl + f'pokemon/{search}')
        if res.content != b'Not Found':
            print("Pokemon founded!")
            pokemon = json.loads(res.content)
            newPokemon = sqlalc.StorePokemon(pokemon['id'], pokemon['name'], pokemon['height'], pokemon['weight'])
            sqlalc.session.merge(newPokemon)
            # Too expensive works but takes too long to add everything to the database
            # updateMovesTable(pokemon['id'], pokemon['moves'])
            sqlalc.session.commit()
        elif search is not None:
            displayNotFound = True
    return render_template("team.html", pokemon=pokemon, displayNotFound=displayNotFound, search=search)

def updateMovesTable(pokemoneid, moves):
    for move in moves:
        res = requests.get(move['move']['url'])
        moveData = json.loads(res.content)
        description = moveData['effect_entries'][0]['effect'].replace("$effect_chance%", str(moveData['effect_chance']))
        if len(description) > 200:
            # truncate descriptions that are too long
            description = description[:200]
        newMove = sqlalc.StoreMove(moveData['id'], typeDictionary.get(moveData['type']['name']), moveData['name'],
                                   description, moveData['accuracy'], moveData['power'])
        newMoveRel = sqlalc.StoreMoveRel(pokemoneid, moveData['id'])
        sqlalc.session.merge(newMove)
        sqlalc.session.merge(newMoveRel)

if __name__ == "__main__":
    app.run(debug=True)
