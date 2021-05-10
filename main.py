from pandas import *
from numpy import nan
from functions import *
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import casinos.fanduel as fd #need to add another import per casino
import casinos.draftkings as dk
import casinos.betmgm as bm


#need to add more lines for each casino and sport which is 'casinosportnames':[]
html_names = {
    'dkufcnames':[],
    'dkmlbnames':[],
    'dknhlnames':[],
    'dknbanames':[],

    'fdufcnames':[],
    'fdmlbnames':[],
    'fdnhlnames':[],
    'fdnbanames':[],
    
    'bmufcnames':[],
    'bmmlbnames':[],
    'bmnhlnames':[],
    'bmnbanames':[],
}

#need to add more lines for each casino and sport which is 'casinosportbets':[]
html_bets = {
    'dkufcbets':[],
    'dkmlbbets':[],
    'dknhlbets':[],
    'dknbabets':[],

    'fdufcbets':[],
    'fdmlbbets':[],
    'fdnhlbets':[],
    'fdnbabets':[],

    'bmufcbets':[],
    'bmmlbbets':[],
    'bmnhlbets':[],
    'bmnbabets':[],
}

#this can change depending on what sport(s) the user wants.
#i.e. this user only wants ufc and mlb
usersports = [
    'ufc',
    'mlb',
    'nhl',
    'nba'
]

#need to add 1 more per casino
CASINO_TAG = {
    'fd':fd, #fanduel
    'bm':bm, #betmbm
    'dk':dk #draftkings
}

#need to add more lines for each new casino and sport which is 'casinosport':('url','nameclass','betclass'),
ALL_HTML_DATA = {
    'dkufc':('https://sportsbook.draftkings.com/leagues/mma/2162?category=fight-lines&subcategory=moneyline','sportsbook-outcome-cell__label','sportsbook-odds american default-color'), 
    'dkmlb':('https://sportsbook.draftkings.com/leagues/baseball/2003?category=game-lines-&subcategory=game','event-cell__name','sportsbook-table__column-row'), 
    'dknhl':('https://sportsbook.draftkings.com/leagues/hockey/2022?category=game-lines&subcategory=game','event-cell__name','sportsbook-table__column-row'), 
    'dknba':('https://sportsbook.draftkings.com/leagues/basketball/103?category=game-lines&subcategory=game','event-cell__name','sportsbook-odds american default-color'),

    'fdufc':('https://sportsbook.fanduel.com/sports/navigation/7287.1/9886.3','selection-name','sh'),
    'fdmlb':('https://sportsbook.fanduel.com/sports/navigation/1110.1/7627.1','name','sh'),
    'fdnhl':('https://sportsbook.fanduel.com/sports/navigation/1550.1/10329.3','name','sh'),
    'fdnba':('https://sportsbook.fanduel.com/sports/navigation/830.1/10107.3','name','sh'),

    'bmufc':('https://sports.mi.betmgm.com/en/sports/mma-45','participant','grid-group-container'),
    'bmmlb':('https://sports.mi.betmgm.com/en/sports/baseball-23/betting/north-america-9/mlb-75','participant','grid-group-container'),
    'bmnhl':('https://sports.mi.betmgm.com/en/sports/ice-hockey-12/betting/north-america-9/nhl-34','participant','grid-group-container'),
    'bmnba':('https://sports.mi.betmgm.com/en/sports/basketball-7/betting/north-america-9/nba-6004','participant','grid-group-container'),
}

COLUMNS = {'Team 1':[nan],'Max Bet1':[nan],'Max Bet1 Casino':[nan],'Max Bet1 Conv':[nan],'Team 2':[nan],'Max Bet2':[nan],'Max Bet2 Casino':[nan],'Max Bet2 Conv':[nan]}
BASEDF = DataFrame(data=COLUMNS)
COLUMNSDRAW = {'Team 1':[nan],'Max Bet1':[nan],'Max Bet1 Casino':[nan],'Max Bet1 Conv':[nan],'Team 2':[nan],'Max Bet2':[nan],'Max Bet2 Casino':[nan],'Max Bet2 Conv':[nan], 'Max Bet Draw':[nan],'Max Bet Draw Casino':[nan],'Max Bet Draw Conv':[nan]}
BASEDFDRAW = DataFrame(data=COLUMNSDRAW) #base dataframe for sports with 3 outcomes

for casinoindex in range(len(CASINO_TAG)):
    BASEDF.insert(1,'Bet1 {}'.format(list(CASINO_TAG.keys())[casinoindex]),nan)
    BASEDF.insert(casinoindex+6,'Bet2 {}'.format(list(CASINO_TAG.keys())[casinoindex]),nan)
    BASEDFDRAW.insert(1,'Bet1 {}'.format(list(CASINO_TAG.keys())[casinoindex]),nan)
    BASEDFDRAW.insert(casinoindex+6,'Bet2 {}'.format(list(CASINO_TAG.keys())[casinoindex]),nan)
    # BASEDFDRAW.insert(casinoindex+?,'Bet3 {}'.format(list(CASINO_TAG.keys())[casinoindex]),nan) #don't know what the ? needs to be

#need to add the sport to the line below, and the sport to the SPORTS dictionary with its new DF and function
ufc, mlb, nhl, nba = BASEDF, BASEDF, BASEDF, BASEDF
SPORTS = {
    'ufc':ufc, 
    'mlb':mlb, 
    'nhl':nhl, 
    'nba':nba
}

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get('https://www.google.com/') #basically initializes the window with this website. All the tabs are then loaded afterwards for easy navigation based on the names

#opening and loading all urls
for casino in CASINO_TAG:
    print('Opening ' + casino)
    for sport in usersports:
        driver.execute_script('window.open("about:blank","{}");'.format(casino + sport))
        driver.switch_to.window(casino + sport)
        driver.get(ALL_HTML_DATA[casino + sport][0])
print('Loading in Web Pages')
time.sleep(45)

#get the data from the urls
for casino in CASINO_TAG:
    print('Reading in ' + casino + ' data')
    for sport in usersports:
        driver.switch_to.window(casino + sport)
        html_bets[casino + sport + 'bets'] = driver.find_elements_by_class_name(ALL_HTML_DATA[casino + sport][2])
        html_names[casino + sport + 'names'] = driver.find_elements_by_class_name(ALL_HTML_DATA[casino + sport][1])
driver.quit()

#sort the data for each casino and sport and create the dataframes for each sport
for casino in CASINO_TAG:
    print('Sorting ' + casino + ' data')
    for sport in usersports:
        print(sport)
        print(html_bets[casino + sport + 'bets'])
        #need to add another elif statement for each new sport
        if sport == 'ufc':
            names1, names2, bets1, bets2 = CASINO_TAG[casino].ufc_data(html_names[casino + sport + 'names'], html_bets[casino + sport + 'bets'])
        elif sport == 'mlb':
            names1, names2, bets1, bets2 = CASINO_TAG[casino].mlb_data(html_names[casino + sport + 'names'], html_bets[casino + sport + 'bets'])
        elif sport == 'nba':
            names1, names2, bets1, bets2 = CASINO_TAG[casino].nba_data(html_names[casino + sport + 'names'], html_bets[casino + sport + 'bets'])
        elif sport == 'nhl':
            names1, names2, bets1, bets2 = CASINO_TAG[casino].nhl_data(html_names[casino + sport + 'names'], html_bets[casino + sport + 'bets'])
        
        SPORTS[sport] = makedf_all(SPORTS[sport], names1, names2, bets1, bets2, casino)

#calculate the arbs for each sport and generate the spreadsheets
for casino in CASINO_TAG:
    print('Calculating ' + casino + ' arbs')
    for sport in usersports:
        SPORTS[sport] = arbs(SPORTS[sport],CASINO_TAG)
        opss(SPORTS[sport])

for sport in usersports:
    print(SPORTS[sport])
