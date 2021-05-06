from functions import *
from pandas import *
from numpy import nan
import casinos.draftkings as dk #need to add 1 import per casino
import casinos.fanduel as fd
import casinos.betmgm as bm


#casino tags. Add a casino tag for each casino
CASINOTAG = ['dk','fd','bm']
CASINOFUNCTIONTAG = [dk,fd,bm]

#make base dataframes used as reference for all future dataframes shouldn't change
COLUMNS = ['Team1','Max Bet1','Max Bet1 Casino','Max Bet1 Conv','Team2','Max Bet2','Max Bet2 Casino','Max Bet2 Conv','Arb Value','Arb']
BASEDF = DataFrame(columns=COLUMNS) #base dataframe for sports with 2 outcomes

COLUMNSDRAW = ['Team1','Max Bet1','Max Bet1 Casino','Max Bet1 Conv','Team2','Max Bet2','Max Bet2 Casino','Max Bet2 Conv',
              'Max Bet Draw','Max Bet Draw Casino','Max Bet Draw Conv','Arb Value','Arb']
BASEDFDRAW = DataFrame(columns=COLUMNSDRAW) #base dataframe for sports with 3 outcomes

for casinoindex in range(len(CASINOTAG)):
    BASEDF.insert(1,'Bet1 {}'.format(CASINOTAG[casinoindex]),nan)
    BASEDF.insert(casinoindex+6,'Bet2 {}'.format(CASINOTAG[casinoindex]),nan)

#add one more 'sport = BASEDF' for each additional sport or 'sport = BASEDFDRAW' for any 3 outcome sport
ufc,nhl,mlb,nba = BASEDF,BASEDF,BASEDF,BASEDF

#making dataframes for each sport. add one more line to the for loop 'sport = makedf_all(sport, CASINOFUNCTIONTAG[i].sport_data(), CASINOTAG[i])' for each additional sport
#or 'sport = makedf_all3outcome(sport, CASINOFUNCTIONTAG[i].sport_data(), CASINOTAG[i])' for any 3 outcome sport
for i in range(len(CASINOFUNCTIONTAG)):
    ufc = makedf_all(ufc, CASINOFUNCTIONTAG[i].ufc_data(), CASINOTAG[i])
    nhl = makedf_all(nhl, CASINOFUNCTIONTAG[i].nhl_data(), CASINOTAG[i])
    mlb = makedf_all(mlb, CASINOFUNCTIONTAG[i].mlb_data(), CASINOTAG[i])
    nba = makedf_all(nba, CASINOFUNCTIONTAG[i].nba_data(), CASINOTAG[i])

#calculating arbs and generating spreadsheets for each sport. Add one more line 'opss(arbs(sport,CASINOS))' for each additional sport
#or 'opss3outcome(arbs3outcome(sport,CASINOTAG))'
opss(arbs(ufc,CASINOTAG))
opss(arbs(nhl,CASINOTAG))
opss(arbs(mlb,CASINOTAG))
opss(arbs(nba,CASINOTAG))

print(ufc)
print(nhl)
print(mlb)
print(nba)
