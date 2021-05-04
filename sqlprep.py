#File for prepared statements
#Main source is in code examples from lecture

from random import randint
import mysql.connector

# Do not forget to install mysql.connector
# pip install mysql-connector-python

import connection_info


#removes the @ and the port from the ip address in connection_info
cnx = mysql.connector.connect(user='root', password=connection_info.MyPassword,
                              host=connection_info.MyHost[1:-6],
                              database=connection_info.MyDatabase)

cursor = cnx.cursor(buffered=True)

def removeFromTeam(team, pokemon):
    #removes pokemon from team
    #teamid = team, pokemonid = pokemon
    stmt1 = "DELETE FROM pokibase.teamrel WHERE teamid =%s and pokemonid=%s"

    #gets count of team
    stmt2 = "SELECT count from pokibase.team where teamid =%s"

    #updates count of team
    #count = new count, teamid = team
    stmt3 = "UPDATE pokibase.team SET count=%s WHERE teamid=%s" #could make this a trigger

    try:
        cursor.execute(stmt1, (team, pokemon))
        cursor.execute(stmt2, (team,))
        cnt = cursor.fetchone()
        
        cnt = cnt[0] - 1
        
        cursor.execute(stmt3, (cnt, team))
        cnx.commit()
    except:
        cnx.rollback()
        print("Error remove from team")

def getMoves(pokemon):
    stmt = "SELECT name FROM move, moverel WHERE move.moveid = moverel.moveid and moverel.pokemonid =%s"
    #maybe change to From move join moverel on move.moveid = moverel.movdie
    try: 
        cursor.execute(stmt, (pokemon,))
    except:
        print("Error getting moves")
    moveSet = []
    for name in cursor:
        #print(str(name)[1:-3])
        moveSet.append(str(name)[2:-3])
    if len(moveSet) == 0:
        moveSet.append("No Moves")
    return moveSet

def getMovesFromName(pokemonID):
    stmt = "SELECT name FROM move, moverel, pokemon WHERE move.moveid = moverel.moveid and moverel.pokemonid = pokemon.pokemonid and pokemonname=%s"
    try:
        cursor.execute(stmt, (pokemonID,))
    except:
        print("Error getting moves")
    moveSet = []
    for name in cursor:
        #print(str(name)[1:-3])
        moveSet.append(str(name)[2:-3])
    if len(moveSet) == 0:
        moveSet.append("No Moves")
    return moveSet

def deleteTeam(teamID):
    stmt1 = "DELETE FROM team WHERE teamid=%s"
    stmt2 = "DELETE FROM teamrel where teamid=%s"

    print("deleteteam")
    try:
        cursor.execute(stmt1, (teamID,))
        cursor.execute(stmt2, (teamID,))
        cnx.commit()
    except:
        cnx.rollback()
        print("Error deleting team")

def getTopFive():
    stmt = """select pokemonname
        from pokibase.pokemon as t1, 
        (select pokemonid, count(teamid) as cnt
        from pokibase.teamrel as p
        group by pokemonid
        order by cnt desc
        limit 5) as t2
        where t1.pokemonid = t2.pokemonid;"""
    try:
        cursor.execute(stmt)
    except:
        print("Error getting top 5 pokemon")
    topFive = []
    for name in cursor:
        topFive.append(name[0])
    if len(topFive) == 0:
        topFive.append("NA")
    return topFive

def aggregateTeamStats(teamID):
    stmt = """
    SELECT avg(hp), avg(atk), avg(defense), avg(spatk), avg(spdef), avg(spd) 
    FROM pokibase.statv2 as s Join pokibase.teamrel as r
    On s.pokemonid = r.pokemonid 
    where r.teamid = %s"""
    try:
        cursor.execute(stmt, (teamID,))
    except:
        print("Error aggregating stats")
    stats = []
    labels = ["hp: ", "atk: ", "defense: ", "spatk: ", "spdef: ", "spd: "]
    for s in cursor:
        print(s)
        for i in range(0,6):
            stats.append(labels[i] + str(s[i]))
    if len(stats) == 0:
        stats.append("NA")
    return stats

def getPokemonFromName(name):
    stmt = "SELECT pokemonid FROM pokibase.pokemon where pokemonname=%s;"
    try:
        cursor.execute(stmt, (name,))
    except:
        print("Error getting pokemon")
    return cursor.fetchone()[0]

def getMoveIDFromMoveName(name):
    stmt = "SELECT moveid FROM pokibase.move where name =%s;"
    try:
        cursor.execute(stmt, (name,))
    except:
        print("Error getting moveID")
    x = cursor.fetchone()
    #print
    if x is None:
        x = -1
    else:
        x = x[0]
    return x

def updateMovesinTeamRel(team, pokemon, m1, m2, m3, m4):
    stmt = """
        Update pokibase.teamrel
        Set moveid1=%s, moveid2=%s, moveid3=%s, moveid4=%s
        where teamid =%s and pokemonid =%s ;
        """
    try:
        cursor.execute(stmt, (m1, m2, m3, m4, team, pokemon))
        cnx.commit()
    except:
        print("Error updating moves")

def getTopMoves():
    stmt = """
    select moveid, name, cnt 
    from (
    select moveid, name, count(*) as cnt
    from (select moveid1 as moves
    from pokibase.teamrel
    union all
    select moveid2
    from pokibase.teamrel
    union all
    select moveid3
    from pokibase.teamrel
    union all
    select moveid4
    from pokibase.teamrel) as t1, pokibase.move as t2
    where t1.moves = t2.moveid
    group by moveid) as t4
    having cnt = (select  max(cnt)
    from (
    select name, count(*) as cnt
    from (select moveid1 as moves
    from pokibase.teamrel
    union all
    select moveid2
    from pokibase.teamrel
    union all
    select moveid3
    from pokibase.teamrel
    union all
    select moveid4
    from pokibase.teamrel) as t1, pokibase.move as t2
    where t1.moves = t2.moveid
    group by name ) as t3) ;
    """
    
def getTopFiveMoves():
    stmt = """select name
    from (
    select moveid, count(*) as cnt, name
    from (select moveid1 as moves
    from pokibase.teamrel
    union all
    select moveid2
    from pokibase.teamrel
    union all
    select moveid3
    from pokibase.teamrel
    union all
    select moveid4
    from pokibase.teamrel) as t1, pokibase.move as t2
    where t1.moves = t2.moveid
    group by moveid
    order by cnt desc) as t3
    limit 5; """

    try: 
        cursor.execute(stmt)
    except:
        print("Error getting top 5 moves")
    topFive = []
    for move in cursor:
        topFive.append(move[0])
    if len(topFive) == 0:
        topFive.append("NA")
    return topFive
    
def getTeams():
    stmt = "SELECT DISTINCT teamid FROM teamrel"
    cursor.execute(stmt)
    team_ids = []
    #print(cursor)
    if cursor.rowcount == 0:
        team_ids.append(-1)
        return team_ids
    for team in cursor:
        #print("TEAM ID:" + str(team)[1:2])
        team_ids.append(str(team)[1:2])
        
    return team_ids

def getTeamPokemon(teamId):
    stmt = "SELECT DISTINCT p.pokemonname FROM teamrel t JOIN pokemon p on t.pokemonid = p.pokemonid WHERE t.teamid =%s"
    cursor.execute(stmt, (teamId,))
    pokemon_names = []
    for pokemon in cursor:
        print(str(pokemon)[2:len(str(pokemon))-3])
        pokemon_names.append(str(pokemon)[2:len(str(pokemon))-3])
    
    return pokemon_names

def getNumberForTeamID(maxTeams):
    stmt = "SELECT teamid FROM pokibase.team;"
    try:
        cursor.execute(stmt)
        cnx.commit()
    except:
        print("Error getting number for teamID")
    setOfTeams = set()
    potentialTeams = set()
    for t in cursor:
        #print(t)
        setOfTeams.add(t[0])
    for i in range(1, maxTeams + 1):
        potentialTeams.add(i)
    unusedTeams = potentialTeams - setOfTeams
    print(setOfTeams)
    print("unused teams:")
    print(unusedTeams)
    if len(unusedTeams) == 0:
        newID = randint(1,maxTeams)
        print(newID)
        deleteTeam(newID)
        return newID
    else:
        return next(iter(unusedTeams))
        