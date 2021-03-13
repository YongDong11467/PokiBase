from flask import Flask, render_template, url_for, request
import sqlalc
import requests
import json
app = Flask(__name__)

baseUrl = 'https://pokeapi.co/api/v2/'
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
        if res.content != b'Not Found':
            print("Pokemon founded!")
            pokemon = json.loads(res.content)
            newPokemon = sqlalc.StorePokemon(pokemon['id'], pokemon['name'], pokemon['height'], pokemon['weight'])
            sqlalc.session.merge(newPokemon)
            sqlalc.session.commit()
        elif search is not None:
            displayNotFound = True
    return render_template("team.html", pokemon=pokemon, displayNotFound=displayNotFound, search=search)

if __name__ == "__main__":
    app.run(debug=True)