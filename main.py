from functions import *
from pandas import *
from numpy import nan
import draftkings as dk
import fanduel as fd
import betmgm as bm

#casino tags. Add a casino tag for each casino
CASINOS = ['dk','fd','bm']

#arrays full of the functions for each casino and sport. Need to add 1 array per sport and 1 item to each array for each casino
UFCFUNCTIONS = [dk.ufc_data,fd.ufc_data,bm.ufc_data]
NHLFUNCTIONS = [dk.nhl_data,fd.nhl_data,bm.nhl_data]
MLBFUNCTIONS = [dk.mlb_data,fd.mlb_data,bm.mlb_data]
NBAFUNCTIONS = [dk.nba_data,fd.nba_data,bm.nba_data]

#make base dataframes used as reference for all future dataframes shouldn't change
COLUMNS = ['Team1','Max Bet1','Max Bet1 Casino','Max Bet1 Conv','Team2','Max Bet2','Max Bet2 Casino','Max Bet2 Conv','Arb Value','Arb']
BASEDF = DataFrame(columns=COLUMNS)

COLUMNSDRAW = ['Team1','Max Bet1','Max Bet1 Casino','Max Bet1 Conv','Team2','Max Bet2','Max Bet2 Casino','Max Bet2 Conv',
              'Max Bet Draw','Max Bet Draw Casino','Max Bet Draw Conv','Arb Value','Arb']
BASEDFDRAW = DataFrame(columns=COLUMNSDRAW)

for casinoindex in range(len(CASINOS)):
    BASEDF.insert(1,'Bet1 {}'.format(CASINOS[casinoindex]),nan)
    BASEDF.insert(casinoindex+6,'Bet2 {}'.format(CASINOS[casinoindex]),nan)

#add one more 'sport = BASEDF' for each additional sport or 'sport = BASEDFDRAW' for any 3 outcome sport
ufc,nhl,mlb,nba = BASEDF,BASEDF,BASEDF,BASEDF

#making dataframes for each sport. add one more line to the for loop 'sport = makedf_all(sport, SPORTFUNC[i], CASINOS[i])' for each additional sport
#or 'sport = makedf_all3outcome(sport, SPORTFUNC[i], CASINOS[i])' for any 3 outcome sport
for i in range(len(CASINOS)):
    ufc = makedf_all(ufc, UFCFUNCTIONS[i](), CASINOS[i])
    nhl = makedf_all(nhl, NHLFUNCTIONS[i](), CASINOS[i])
    mlb = makedf_all(mlb, NHLFUNCTIONS[i](), CASINOS[i])
    nba = makedf_all(nba, NHLFUNCTIONS[i](), CASINOS[i])

#calculating arbs and generating spreadsheets for each sport. Add one more line 'opss(arbs(sport,CASINOS))' for each additional sport
#or 'opss3outcome(arbs3outcome(sport,CASINOS))'
opss(arbs(ufc,CASINOS))
opss(arbs(nhl,CASINOS))
opss(arbs(mlb,CASINOS))
opss(arbs(nba,CASINOS))

print(ufc)
print(nhl)
print(mlb)
print(nba)
