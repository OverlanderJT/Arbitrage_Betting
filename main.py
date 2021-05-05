from functions import *
from pandas import *
from numpy import nan
import draftkings as dk
import fanduel as fd
import betmgm as bm

#casino tags. Add a casino tag for each casino
CASINOS = ['dk','fd','bm']

#make base dataframe used as reference for all future dataframes shouldn't change
COLUMNS = ['Team1','Max Bet1','Max Bet1 Casino','Max Bet1 Conv','Team2','Max Bet2','Max Bet2 Casino','Max Bet2 Conv','Arb Value','Arb']
BASEDF = DataFrame(columns=COLUMNS)

for casinoindex in range(len(CASINOS)):
    BASEDF.insert(1,'Bet1 {}'.format(CASINOS[casinoindex]),nan)
    BASEDF.insert(casinoindex+6,'Bet2 {}'.format(CASINOS[casinoindex]),nan)

#need to add one line to each of these groups for every new casino which should be
#SPORT = makedf_all(SPORT, casino.SPORT_data(),'casino')
ufc = BASEDF
ufc = makedf_all(ufc, dk.ufc_data(),'dk')
ufc = makedf_all(ufc, fd.ufc_data(),'fd')
ufc = makedf_all(ufc, bm.ufc_data(),'bm')
ufc = arbs(ufc, CASINOS)
opss(ufc)

nhl = BASEDF
nhl = makedf_all(nhl, dk.nhl_data(),'dk')
nhl = makedf_all(nhl, fd.nhl_data(),'fd')
nhl = makedf_all(nhl, bm.nhl_data(),'bm')
nhl = arbs(nhl, CASINOS)
opss(nhl)

mlb = BASEDF
mlb = makedf_all(mlb, dk.mlb_data(),'dk')
mlb = makedf_all(mlb, fd.mlb_data(),'fd')
mlb = makedf_all(mlb, bm.mlb_data(),'bm')
mlb = arbs(mlb, CASINOS)
opss(mlb)

nba = BASEDF
nba = makedf_all(nba, dk.nhl_data(),'dk')
nba = makedf_all(nba, fd.nhl_data(),'fd')
nba = makedf_all(nba, bm.nhl_data(),'bm')
nba = arbs(nba, CASINOS)
opss(nba)

