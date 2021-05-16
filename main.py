from pandas import DataFrame
from numpy import nan
from functions import makedf_all, makedf_all3outcome, arbs, arbs3outcome, opss, opss3outcome
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from copy import deepcopy
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
#i.e. this user only wants ufc, mlb, and nba
usersports = [
    'ufc',
    'mlb',
    # 'nhl',
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

#stores the window handles to access the windows for each sport and casino later. have to add more for each new casino and sport
window_handles = {
    'dkufc':[],
    'dkmlb':[],
    'dknhl':[],
    'dknba':[],

    'fdufc':[],
    'fdmlb':[],
    'fdnhl':[],
    'fdnba':[],

    'bmufc':[],
    'bmmlb':[],
    'bmnhl':[],
    'bmnba':[],
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

#need to add the sport to the dict below with a copy of its base dataframe "'sport':deepcopy(BASEDF)" or "'sport' = deepcopy(BASEDFDRAW)"
SPORTS = {
    'ufc':deepcopy(BASEDF),
    'mlb':deepcopy(BASEDF),
    'nhl':deepcopy(BASEDF),
    'nba':deepcopy(BASEDF)
}

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get('https://www.google.com/') #basically initializes the window with this website. All the tabs are then loaded afterwards for easy navigation based on the names

#opening and loading all urls
for casino in CASINO_TAG:
    for sport in usersports:
        print('Opening ' + casino + ' ' + sport)
        driver.switch_to.new_window(casino + sport)
        driver.get(ALL_HTML_DATA[casino + sport][0])
        window_handles[casino + sport] = driver.current_window_handle
print('Loading in Web Pages')
time.sleep(25) #wait time to make sure that all pages are loaded in

#get the data from the urls
for casino in CASINO_TAG:
    for sport in usersports:
        print('Reading in ' + casino + ' ' + sport + ' data')
        print(driver.current_window_handle) #debug
        print(window_handles[casino + sport]) #debug
        driver.switch_to.window(window_handles[casino + sport])
        html_bets[casino + sport + 'bets'] = driver.find_elements_by_class_name(ALL_HTML_DATA[casino + sport][2])
        html_names[casino + sport + 'names'] = driver.find_elements_by_class_name(ALL_HTML_DATA[casino + sport][1])
driver.quit()

#sort the data for each casino and sport and create the dataframes for each sport
for casino in CASINO_TAG:
    for sport in usersports:
        print('Sorting ' + casino + ' ' + sport + ' data')
        # print(html_bets[casino + sport + 'bets']) #debug
        #need to add another elif statement for each new sport
        if sport == 'ufc':
            names1, names2, bets1, bets2 = CASINO_TAG[casino].ufc_data(html_names[casino + sport + 'names'], html_bets[casino + sport + 'bets'])
            SPORTS[sport] = makedf_all(SPORTS[sport], names1, names2, bets1, bets2, casino)
        elif sport == 'mlb':
            names1, names2, bets1, bets2 = CASINO_TAG[casino].mlb_data(html_names[casino + sport + 'names'], html_bets[casino + sport + 'bets'])
            SPORTS[sport] = makedf_all(SPORTS[sport], names1, names2, bets1, bets2, casino)
        elif sport == 'nba':
            names1, names2, bets1, bets2 = CASINO_TAG[casino].nba_data(html_names[casino + sport + 'names'], html_bets[casino + sport + 'bets'])
            SPORTS[sport] = makedf_all(SPORTS[sport], names1, names2, bets1, bets2, casino)
        elif sport == 'nhl':
            names1, names2, bets1, bets2 = CASINO_TAG[casino].nhl_data(html_names[casino + sport + 'names'], html_bets[casino + sport + 'bets'])
            SPORTS[sport] = makedf_all(SPORTS[sport], names1, names2, bets1, bets2, casino)
        # elif sport == 'soccer':
        #     names1, names2, bets1, bets2, bets3 = CASINO_TAG[casino].soccer_data(html_names[casino + sport + 'names'], html_bets[casino + sport + 'bets'])
        #     SPORTS[sport] = makedf_all3outcome(SPORTS[sport], names1, names2, bets1, bets2, bets3, casino)
        else:
            print('Unimplemented Sport') #this should never happen

#calculate the arbs for each sport and generate the spreadsheets
for casino in CASINO_TAG:
    for sport in usersports:
        print('Calculating ' + casino + ' ' + sport + ' arbs')
        #need to add each additional sport to the relevent if statement
        if sport == 'ufc' or sport == 'mlb' or sport == 'nba' or sport == 'nhl': #for any sport with only Win/Loss
            SPORTS[sport] = arbs(SPORTS[sport],CASINO_TAG)
            opss(SPORTS[sport])
        # elif sport == 'soccer': #for any sport with Win/Loss/Draw
        #     SPORTS[sport] = arbs3outcome(SPORTS[sport],CASINO_TAG)
        #     opss3outcome(SPORTS[sport])
        else:
            print('Unimplemented Sport') #this should never happen

#print all sport data
for sport in usersports:
    print(SPORTS[sport])
    # print(SPORTS[sport].loc['Arb'==True]) #only prints the games that have profitable arbs
    # print(SPORTS[sport][['Team1' 'Max Bet1', 'Max Bet1 Casino', 'Team2', 'Max Bet2', 'Arb value']].loc['Arb'==True]) #only print relevant columns with profitable arbs
    # print(SPORTS[sport][['Team1' 'Max Bet1', 'Max Bet1 Casino', 'Team2', 'Max Bet2', 'Max Bet Draw', 'Max Bet Draw Casino', 'Arb value']].loc['Arb'==True]) #only print relevant columns with profitable arbs for 3 outcome sports
