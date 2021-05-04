from flask import Flask, render_template, url_for, request, session, redirect
from sqlalchemy.sql.type_api import NULLTYPE
import sqlalc
import requests
import json
import sqlprep
app = Flask(__name__)
app.secret_key = "qwertyuiop"
from random import randint

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

#pokemonid of last searched, used for add to team
#if add to team must be most recently searched
mostRecentPokemon = -1

#Sets number of possible teams in the database
numberOfTeams = 10

#Current team id 
currentTeamID = sqlprep.getNumberForTeamID(numberOfTeams)
print("(Global)currentTeamID: " + str(currentTeamID))

#TODO: Create a session
#TODO: Organize files with blueprint

@app.route('/')
def home():
    team_ids = sqlprep.getTeams()
    if team_ids[0] != -1:
        pokemon_imgs = [] 
        pokemon_names = []
        team_count = 0
        pokemon_count = 0
        for team in team_ids:
            names = sqlprep.getTeamPokemon(team)
            curr_team_imgs = []
            for pokemon in names:
                res = requests.get(baseUrl + f'pokemon/{pokemon}')
                #print("THE FOLLOWING IS BASE URL:\n" + baseUrl + f'pokemon/{pokemon}')
                if res.content != b'Not Found':
                    #print("hi")
                    curr_pokemon = json.loads(res.content)
                    curr_team_imgs.append(curr_pokemon["sprites"]["front_default"])
                else :
                    print("bye")
                pokemon_count = pokemon_count+1
            team_count = team_count + 1
            pokemon_imgs.append(curr_team_imgs)
            pokemon_names.append(names)
        return render_template("home.html", teams = team_ids, teamnames = pokemon_names, teamimgs = pokemon_imgs)

    else:
        print("bye2")
        return render_template("home.html", teams = None, teamimgs = None)

@app.route('/team', methods=['GET', 'POST'])
def team():
    if not 'curteam' in session:
        session['curteam'] = []
    if not 'curteamimg' in session:
        session['curteamimg'] = []

    curteam = session['curteam']
    curteamimg = session['curteamimg']
    search = None
    displayNotFound = False
    pokemon = None
    move = None
    ability = None
    # session['curpokemon'] = "troll"
    if request.method == "GET":
        search = request.args.get("search")
        option = request.args.get('inlineRadioOptions')
        print(option)
        if option == 'Pokemon':
            res = requests.get(baseUrl + f'pokemon/{search}')
            print("THE FOLLOWING IS BASE URL:\n" + baseUrl + f'pokemon/{search}')
            #print("SEARCH:" + search)
            if res.content != b'Not Found':
                print("Pokemon founded!")
                pokemon = json.loads(res.content)
                # statid = randint(1, 10000)
                session['curpokemon'] = pokemon["name"]
                session['curimageRef'] = pokemon["sprites"]["front_default"]
                newPokemon = sqlalc.StorePokemon(pokemon['id'], pokemon['name'], pokemon['height'], pokemon['weight'])
                sqlalc.session.merge(newPokemon)
                # Moves is too expensive works but takes too long to add everything to the database
                # updateMovesTable(pokemon['id'], pokemon['moves'])
                updateAbilityTable(pokemon['id'], pokemon['abilities'])
                updateTypeTable(pokemon['id'], pokemon['types'])
                updateStatTable(pokemon['id'], pokemon['stats'])
                sqlalc.session.commit()
                #sets most recently searched
                global mostRecentPokemon
                mostRecentPokemon = pokemon['id']
            elif search is not None:
                displayNotFound = True
        elif option == 'Move':
            #print("Getting move")
            move = sqlalc.getMove(search)
            if not move:
                move = None
                displayNotFound = True
            # res = requests.get(baseUrl + f'move/{search}')
            # print(baseUrl + f'move/{search}')
            # if res.content != b'Not Found':
            #     print("Move founded!")
            #     move = json.loads(res.content)
            #     print(move)
        elif option == 'Ability':
            ability = sqlalc.getAbility(search)
    if request.method == "POST": 
        print(request.form)
        #print("remove")

        #the entire team is gone
        if len(curteam) == 1:
            return redirect(url_for("clearteam"))
        index = int(request.form["remove"])
        removePokemon = curteam[index]
        remove_id = sqlprep.getPokemonFromName(removePokemon)
        
        
        #removes pokemon
        curteam.pop(index)
        curteamimg.pop(index)
        session['curteam'] = curteam
        session['curteamimg'] = curteamimg
        sqlprep.removeFromTeam(currentTeamID, remove_id)
        print("finished")
        return redirect(url_for("team"))
    return render_template("team.html", pokemon=pokemon, move=move, ability=ability,
                           displayNotFound=displayNotFound, search=search, curteam=curteam, curteamimg=curteamimg)

@app.route('/addtoteam')
def addtoteam():
    #print("in add team")
    if not 'curteam' in session:
        session['curteam'] = []
    if not 'curteamimg' in session:
        session['curteamimg'] = []

    curteam = session['curteam']
    curteamimg = session['curteamimg']

    if len(curteam) > 5:
        return redirect(url_for("team"))

    if 'curpokemon' in session:
        #print("in if")
        curteam.append(session['curpokemon'])
        session['curteam'] = curteam
        #print(session["curteam"])
        # print(session["curteam"]["sprites"]["front_default"])
        #adds to team and teamid sql tables
        global currentTeamID
        newTeamMember = sqlalc.AddToTeam(currentTeamID, len(curteam))
        newTeamMemberRel = sqlalc.AddToTeamRel(mostRecentPokemon, currentTeamID, "-1", "-1", "-1", "-1")
        sqlalc.session.merge(newTeamMember)
        sqlalc.session.merge(newTeamMemberRel)
        sqlalc.session.commit()
    if 'curimageRef' in session:
        curteamimg.append(session['curimageRef'])
        session['curteamimg'] = curteamimg
        #print(session["curteamimg"])
    return redirect(url_for("team"))

@app.route('/clearteam')
def clearteam():
    session.pop("curteam", None)
    session.pop("curteamimg", None)
    sqlprep.deleteTeam(currentTeamID)
    return redirect(url_for("team"))

@app.route('/commentonteam')
def commentonteam():
    return redirect(url_for("home"))

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
    
def updateAbilityTable(pokemoneid, abilities):
    for ability in abilities:
        res = requests.get(ability['ability']['url'])
        abilityData = json.loads(res.content)
        description = abilityData['effect_entries'][1]['effect']
        if len(description) > 200:
            # truncate descriptions that are too long
            description = description[:200]
        newAbility = sqlalc.StoreAbility(abilityData['id'], abilityData['name'], description)
        newAbilityRel = sqlalc.StoreAbilityRel(pokemoneid, abilityData['id'])
        sqlalc.session.merge(newAbility)
        sqlalc.session.merge(newAbilityRel)

def updateTypeTable(pokemonid, types):
    for type in types:
        print(type)
        newType = sqlalc.StoreType(typeDictionary[type['type']['name']], type['type']['name'])
        newTypeRel = sqlalc.StoreTypeRel(pokemonid, typeDictionary[type['type']['name']])
        sqlalc.session.merge(newType)
        sqlalc.session.merge(newTypeRel)

def updateStatTable(pokemonid, stats):
    newStat = sqlalc.StoreStat(pokemonid, stats[0]['base_stat'], stats[1]['base_stat'], stats[2]['base_stat'],
                               stats[3]['base_stat'], stats[4]['base_stat'], stats[5]['base_stat'])
    sqlalc.session.merge(newStat)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if not 'curteam' in session:
        session['curteam'] = []
    if not 'curteamimg' in session:
        session['curteamimg'] = []

    curteam = session['curteam']
    curteamimg = session['curteamimg']

    curTeamSet2 = [] 
   
   #array of movesets for each pokemon in the team
    for pokemon in curteam:
        moveSet = sqlprep.getMovesFromName(pokemon)
        curTeamSet2.append(moveSet)

    topFive = sqlprep.getTopFive()
    topFiveMoves = sqlprep.getTopFiveMoves()
    stats = sqlprep.aggregateTeamStats(currentTeamID)

    #finds pokemon to get removed and edits moves
    if request.method == "POST": 
        print(request.form)
        #get what type of request it is
        #gets the key and then uses it to get value
        res2 = list(request.form)[0]
        #need to check to see if not remove
        #it's b/c remove only has index 0
        #thus following 3 lines could cause out of bounds
        res1 = "no"
        if res2 != "remove":
            res1 = list(request.form)[4]
        
        
        if(res1 == "moves"):
            print("moves")
            #gets dictionary keys for moves (moves are the value)
            s = []
            for i in range(0,4):
                s.append(list(request.form)[i])
            

            #gets index in curteam
            print(s[0])
            index = int(s[0][0])
            #index = index[0]
            print(index)
            movesPokemon = curteam[index]
            
            #gets ID of pokemon
            print(movesPokemon)
            movesPokemonID = sqlprep.getPokemonFromName(movesPokemon)
            pickedMoves = []

            #get move id's
            for i in range(0,4):
                print(request.form[s[i]])
                pickedMoves.append(sqlprep.getMoveIDFromMoveName(request.form[s[i]]))

            #update teamrel table
            print(currentTeamID, movesPokemonID, pickedMoves[0], pickedMoves[1], pickedMoves[2], pickedMoves[3])
            sqlprep.updateMovesinTeamRel(currentTeamID, movesPokemonID, pickedMoves[0], pickedMoves[1], pickedMoves[2], pickedMoves[3])

        if res2 == "remove":
            print("remove")

            #the entire team is gone
            if len(curteam) == 1:
                return redirect(url_for("clearteam"))

            index = int(request.form["remove"])
            print((curteam[index]))
            removePokemon = curteam[index]
            remove_id = sqlprep.getPokemonFromName(removePokemon)
            
            
            #removes pokemon
            curteam.pop(index)
            curteamimg.pop(index)
            session['curteam'] = curteam
            session['curteamimg'] = curteamimg
            sqlprep.removeFromTeam(currentTeamID, remove_id)
            print("finished")
            return redirect(url_for("edit"))
        
  
    return render_template("edit.html", curteamimg=curteamimg, curteam = curteam, curTeamSet2 = curTeamSet2, topFive=topFive, topFiveMoves = topFiveMoves, stats = stats)


@app.route("/submitTeam")
def submitTeam():
    print("submittingteam")
    global currentTeamID
    global numberOfTeams
    currentTeamID = sqlprep.getNumberForTeamID(numberOfTeams)
    print("new team: " + str(currentTeamID))
    session.pop("curteam", None)
    session.pop("curteamimg", None)
    return redirect(url_for("team"))

if __name__ == "__main__":
    app.run(debug=True)
