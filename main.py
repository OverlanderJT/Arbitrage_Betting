from functions import *
from pandas import DataFrame
from numpy import nan
import casinos.draftkings as dk #need to add 1 import per casino
import casinos.fanduel as fd
import casinos.betmgm as bm


#casino tags. Add a casino tag for each casino
CASINOTAG = ('dk','fd','bm')
CASINOFUNCTIONTAG = (dk,fd,bm)

#make base dataframes used as reference for all future dataframes shouldn't change
COLUMNS = {'Team 1':[nan],'Max Bet1':[nan],'Max Bet1 Casino':[nan],'Max Bet1 Conv':[nan],'Team 2':[nan],'Max Bet2':[nan],'Max Bet2 Casino':[nan],'Max Bet2 Conv':[nan],'Arb':[nan]}
BASEDF = DataFrame(data=COLUMNS) #base dataframe for sports with 2 outcomes

COLUMNSDRAW = {'Team 1':[nan],'Max Bet1':[nan],'Max Bet1 Casino':[nan],'Max Bet1 Conv':[nan],'Team 2':[nan],'Max Bet2':[nan],'Max Bet2 Casino':[nan],'Max Bet2 Conv':[nan],
              'Max Bet Draw':[nan],'Max Bet Draw Casino':[nan],'Max Bet Draw Conv':[nan],'Arb Value':[nan],'Arb':[nan]}
BASEDFDRAW = DataFrame(data=COLUMNSDRAW) #base dataframe for sports with 3 outcomes

for casinoindex in range(len(CASINOTAG)):
    BASEDF.insert(1,'Bet1 {}'.format(CASINOTAG[casinoindex]),nan)
    BASEDF.insert(casinoindex+6,'Bet2 {}'.format(CASINOTAG[casinoindex]),nan)

#add one more 'sport = BASEDF' for each additional sport or 'sport = BASEDFDRAW' for any 3 outcome sport
ufc,nhl,mlb,nba = BASEDF,BASEDF,BASEDF,BASEDF

#making dataframes for each sport. add two more lines to the for loop
# names1, names2, bets1, bets2 = CASINOFUNCTIONTAG[i].sport_data() or
# names1, names2, bets1, bets2, bets3 = CASINOFUNCTIONTAG[i].sport_data() for 3 outcome sport
# sport = makedf_all(sport, names1, names2, bets1, bets2, CASINOTAG[i]) or
# sport = makedf_all3outcome(sport, names1, names2, bets1, bets2, bets3, CASINOTAG[i]) for 3 outcome sport
for i in range(len(CASINOFUNCTIONTAG)):
    names1, names2, bets1, bets2 = CASINOFUNCTIONTAG[i].ufc_data()
    ufc = makedf_all(ufc, names1, names2, bets1, bets2, CASINOTAG[i])
    names1, names2, bets1, bets2 = CASINOFUNCTIONTAG[i].nhl_data()
    nhl = makedf_all(nhl, names1, names2, bets1, bets2, CASINOTAG[i])
    names1, names2, bets1, bets2 = CASINOFUNCTIONTAG[i].mlb_data()
    mlb = makedf_all(mlb, names1, names2, bets1, bets2, CASINOTAG[i])
    names1, names2, bets1, bets2 = CASINOFUNCTIONTAG[i].nba_data()
    nba = makedf_all(nba, names1, names2, bets1, bets2, CASINOTAG[i])

#calculating arbs and generating spreadsheets for each sport. Add one more line 'opss(arbs(sport,CASINOS))' for each additional sport
#or 'opss3outcome(arbs3outcome(sport,CASINOTAG))'
ufc = arbs(ufc,CASINOTAG)
nhl = arbs(nhl,CASINOTAG)
mlb = arbs(mlb,CASINOTAG)
nba = arbs(nba,CASINOTAG)

opss(ufc)
opss(nhl)
opss(mlb)
opss(nba)

print(ufc)
print(nhl)
print(mlb)
print(nba)
