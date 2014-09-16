import csv

def getStats(owner):
    curpoints = 0
    data = open(owner + '.csv', 'rb')
    reader = csv.reader(data, delimiter=",")
    QB,RB,WR,TE,LB,DL,DB,DLLB,K,Starter = ([],[],[],[],[],[],[],[],[],[])
    line = 0
    pointscolumn = 0
    for row in reader:
        line += 1
        if line == 2:
            i = 0
            for cell in row:
                if cell == 'LAST':
                    pointscolumn = i
                i+= 1      
        elif line not in [1,2,18,19] and row[1] != '':
            name = row[1].split(',')[0]
            position = row[1].split('\xa0')[1]
            points = row[pointscolumn]
            if line > 2 and line < 18:
                curpoints += float(row[pointscolumn])
            if points == '--':
                points = 0

            player = {'name':name,'position':position,'points':points}

            defense = {
                'DE':'DL','DT':'DL','DT, DE':'DL',
                'S':'DB','CB':'DB','CB, S':'DB',
                'DE, LB':'DLLB','LB, DE':'DLLB'
                }
            
            p = player['position']
            if p not in locals():
                p = defense[p]
            eval(p).append(player)        
    data.close()

    Roster = [QB,RB,WR,TE,LB,DL,DB,DLLB,K,Starter]
    i = 0
    for position in Roster:
        if position != []:
            position = sorted(position, key=lambda x:float(x['points']), reverse=True)
        Roster[i] = position
        i += 1

    Roster = SelectBest(Roster)

    TotalPoints = 0
    
    for player in Starter:
        TotalPoints += float(player['points'])
    return [curpoints, TotalPoints]

def SelectBest(Roster):
    RosterPositions = []
    RosterPositions.append(['QB'])
    RosterPositions.append(['RB'])
    RosterPositions.append(['RB'])
    RosterPositions.append(['WR'])
    RosterPositions.append(['WR'])
    
    RosterPositions.append(['TE'])
    RosterPositions.append(['RB','WR','TE']) #Flex 1
    RosterPositions.append(['RB','WR','TE']) #Flex 2
    RosterPositions.append(['QB','RB','WR','TE']) #OP
    RosterPositions.append(['LB','DLLB'])
    
    RosterPositions.append(['DL','DLLB']) #DL
    RosterPositions.append(['DB']) #DB
    RosterPositions.append(['LB','DL','DB','DLLB']) #DP1
    RosterPositions.append(['LB','DL','DB','DLLB']) #DP2
    RosterPositions.append(['K']) #K

    for slot in RosterPositions:
        Roster = ComparePositions(Roster,slot)
    return Roster

def ComparePositions(Roster,Positions):
    # Dictionary for positions in Roster:
    dic = {'QB':0,'RB':1,'WR':2,'TE':3,'LB':4,'DL':5,\
           'DB':6,'DLLB':7,'K':8,'Starter':9}
    first = 1
    best = []

    #Selects  the best player out of all positions selected
    for Position in Positions:
        if Roster[dic[Position]] != []:         
            if first == 1:
               best = dic[Position]
               first = 0
            else:
               if float(Roster[dic[Position]][0]['points']) > float(Roster[best][0]['points']):
                    best = dic[Position]

    Roster[dic['Starter']].append(Roster[best].pop(0))
    return Roster
