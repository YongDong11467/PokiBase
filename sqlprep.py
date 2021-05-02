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
    stmt1 = "DELETE FROM pokibase.teamrel WHERE teamid =%s and pokemonid=%s"

    #gets count of team
    stmt2 = "SELECT count from pokibase.team where teamid =%s"

    #updates count of team
    #count = new count, teamid = team
    stmt3 = "UPDATE pokibase.team SET count=%s WHERE teamid=%s" #could make this a trigger

    cursor.execute(stmt1, (team, pokemon))
    cursor.execute(stmt2, (team,))
    cnt = cursor.fetchone()
    
    cnt = cnt[0] - 1
    
    cursor.execute(stmt3, (cnt, team))
    cnx.commit()

def getMoves(pokemon):
    stmt = "SELECT name FROM move, moverel WHERE move.moveid = moverel.moveid and moverel.pokemonid =%s"
    #maybe change to From move join moverel on move.moveid = moverel.movdie
    cursor.execute(stmt, (pokemon,))
    moveSet = []
    for name in cursor:
        #print(str(name)[1:-3])
        moveSet.append(str(name)[2:-3])
    if len(moveSet) == 0:
        moveSet.append("No Moves")
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

def deleteTeam(teamID):
    stmt1 = "DELETE FROM team WHERE teamid=%s"
    stmt2 = "DELETE FROM teamrel where teamid=%s"

    print("deleteteam")

    cursor.execute(stmt1, (teamID,))
    cursor.execute(stmt2, (teamID,))
    cnx.commit()

def getTopFive():
    stmt = """select pokemonname
        from pokibase.pokemon as t1, 
        (select pokemonid, count(teamid) as cnt
        from pokibase.teamrel as p
        group by pokemonid
        order by cnt desc
        limit 5) as t2
        where t1.pokemonid = t2.pokemonid;"""
    cursor.execute(stmt)
    topFive = []
    for name in cursor:
        topFive.append(name[0])
    if len(topFive) == 0:
        topFive.append("NA")
    return topFive

def aggregateTeam(team):
    stmt = """select *
    from pokibase.pokemon as p, pokibase.teamrel as r, pokibase.team as t
    where p.pokemonid = r.pokemonid and r.teamid = t.teamid and t.teamid = 2;"""

def getPokemonFromName(name):
    stmt = "SELECT pokemonid FROM pokibase.pokemon where pokemonname=%s;"
    cursor.execute(stmt, (name,))
    return cursor.fetchone()[0]

def getMoveIDFromMoveName(name):
    stmt = "SELECT moveid FROM pokibase.move where name =%s;"
    cursor.execute(stmt, (name,))
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
    cursor.execute(stmt, (m1, m2, m3, m4, team, pokemon))
    cnx.commit()

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

    cursor.execute(stmt)
    topFive = []
    for move in cursor:
        topFive.append(move[0])
    if len(topFive) == 0:
        topFive.append("NA")
    return topFive