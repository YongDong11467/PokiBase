#File for prepared statements
#Main source is in code examples from lecture

import mysql.connector

# Do not forget to install mysql.connector
# pip install mysql-connector-python

import connection_info


#removes the @ and the port from the ip address in connection_info
cnx = mysql.connector.connect(user='root', password=connection_info.MyPassword,
                              host=connection_info.MyHost[1:-6],
                              database=connection_info.MyDatabase)

cursor = cnx.cursor()

def removeFromTeam(team, pokemon):
    #removes pokemon from team
    #teamid = team, pokemonid = pokemon
    stmt1 = "DELETE FROM teamrel WHERE teamid =%s and pokemonid=%s"

    #gets count of team
    stmt2 = "SELECT count from team where teamid =%s"
    #updates count of team
    #count = new count, teamid = team
    stmt3 = "UPDATE team SET count=%s WHERE teamid=%s" #could make this a trigger

    cursor.execute(stmt1, (team, pokemon))
    cnx.commit()

def getMoves(pokemon):
    stmt = "SELECT name FROM move, moverel WHERE move.moveid = moverel.moveid and moverel.pokemonid =%s"
    cursor.execute(stmt, (pokemon,))
    moveSet = []
    for name in cursor:
        #print(str(name)[1:-3])
        moveSet.append(str(name)[2:-3])
    return moveSet

def getMovesFromName(pokemonID):
    stmt = "SELECT name FROM move, moverel, pokemon WHERE move.moveid = moverel.moveid and moverel.pokemonid = pokemon.pokemonid and pokemonname=%s"
    cursor.execute(stmt, (pokemonID,))
    moveSet = []
    for name in cursor:
        #print(str(name)[1:-3])
        moveSet.append(str(name)[2:-3])
    if len(moveSet) == 0:
        moveSet.append("No Moves")
    return moveSet