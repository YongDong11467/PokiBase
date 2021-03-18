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

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    #if request.method == "GET":

    #finds pokemon to get removed
    #TODO add backend functionality
    if request.method == "POST":   
        if request.form["remove"] == "0":
           print("Remove0")
        if request.form["remove"] == "1":
           print("Remove1")
        if request.form["remove"] == "2":
           print("Remove2")
        if request.form["remove"] == "3":
           print("Remove3")
        if request.form["remove"] == "4":
           print("Remove4")
        if request.form["remove"] == "5":
           print("Remove5")   
    return render_template("edit.html")    

if __name__ == "__main__":
    app.run(debug=True)