from pandas import DataFrame
from numpy import nan
from functions import Casino, makedf_all, makedf_all3outcome, arbs, arbs3outcome, opss, opss3outcome
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from copy import deepcopy
import os
import casinos.fanduel as fd #need to add another import per casino
import casinos.draftkings as dk
import casinos.betmgm as bm
import casinos.betrivers as br


clear = lambda: os.system('cls') #creating the function to clear the terminal for user friendliness
clear()
#prompts the user to input what sports they want
usersports = []
q = False
sportoptions = ['ufc', 'nba','nhl','mlb', 'mls'] #need to add each new sport to this list
while (q == False):
    if len(sportoptions) == 0:
        break
    entry = input('What sports would you like to arb?  q to quit\n' + ', '.join(sportoptions) + '\n')
    clear()
    if entry == 'q':
         break
    if entry in sportoptions:
        usersports.append(entry)
        del sportoptions[sportoptions.index(entry)]
    elif entry in usersports:
        print('Duplicate Entry')
    else:
        print('Invalid entry')
    
print('Selected Sports')
print(usersports)

fanduel = Casino(
    usersports, 
    tag=('fd', fd),
    html_data={
        'ufc':('https://sportsbook.fanduel.com/sports/navigation/7287.1/9886.3', 'selection-name', 'sh'),
        'mlb':('https://sportsbook.fanduel.com/sports/navigation/1110.1/7627.1', 'name', 'sh'),
        'nhl':('https://sportsbook.fanduel.com/sports/navigation/1550.1/10329.3', 'name', 'sh'),
        'nba':('https://sportsbook.fanduel.com/sports/navigation/830.1/10107.3', 'name', 'sh'),
        'mls':('https://sportsbook.fanduel.com/sports/navigation/730.1/9507.1', 'name', 'sh'),
    }
)

betmgm = Casino(
    usersports, 
    tag=('bm', bm),
    html_data={
        'ufc':('https://sports.mi.betmgm.com/en/sports/mma-45', 'participant', 'grid-group-container'),
        'mlb':('https://sports.mi.betmgm.com/en/sports/baseball-23/betting/north-america-9/mlb-75', 'participant', 'grid-group-container'),
        'nhl':('https://sports.mi.betmgm.com/en/sports/ice-hockey-12/betting/north-america-9/nhl-34', 'participant', 'grid-group-container'),
        'nba':('https://sports.mi.betmgm.com/en/sports/basketball-7/betting/north-america-9/nba-6004', 'participant', 'grid-group-container'),
        'mls':('https://sports.mi.betmgm.com/en/sports/football-4/betting/north-america-9/mls-33155', 'participant', 'grid-group-container'),
    }
)

draftkings = Casino(
    usersports,
    tag=('dk', dk),
    html_data={
        'ufc':('https://sportsbook.draftkings.com/leagues/mma/2162?category=fight-lines&subcategory=moneyline','sportsbook-outcome-cell__label','sportsbook-outcome-cell__element'), 
        'mlb':('https://sportsbook.draftkings.com/leagues/baseball/2003?category=game-lines-&subcategory=game','event-cell__name','sportsbook-table__column-row'), 
        'nhl':('https://sportsbook.draftkings.com/leagues/hockey/2022?category=game-lines&subcategory=game','event-cell__name','sportsbook-table__column-row'), 
        'nba':('https://sportsbook.draftkings.com/leagues/basketball/103?category=game-lines&subcategory=game','event-cell__name','sportsbook-table__column-row'),
        'mls':('https://sportsbook.draftkings.com/leagues/soccer/101?category=game-lines&subcategory=money-line-(regular-time)', 'sportsbook-event-accordion__title', 'sportsbook-outcome-cell'),
    }
)

betrivers = Casino(
    usersports,
    tag = ('br', br),
    html_data={
        'ufc':('https://mi.betrivers.com/?page=sportsbook&group=1000093883&type=prematch#home','participant--name', 'outcome-value'),
        'mlb':('https://mi.betrivers.com/?page=sportsbook&group=1000093616&type=prematch#home','participant--name', 'outcome-value'),
        'nhl':('https://mi.betrivers.com/?page=sportsbook&group=1000093657&type=prematch#home','participant--name', 'outcome-value'),
        'nba':('https://mi.betrivers.com/?page=sportsbook&group=1000093652&type=prematch#home','participant--name', 'outcome-value'),
        'mls':('https://mi.betrivers.com/?page=sportsbook&group=1000095063&type=prematch#home','participant--name', 'outcome-value'),
    }
)

betriverslive = Casino( #this casino is for betrivers live games since they happen at a seperate url
    usersports,
    tag = ('br', br),
    html_data={
        'ufc':('https://mi.betrivers.com/?page=sportsbook&group=1000093883&type=live#home','participant--name', 'outcome-value'),
        'mlb':('https://mi.betrivers.com/?page=sportsbook&group=1000093616&type=live#home','participant--name', 'outcome-value'),
        'nhl':('https://mi.betrivers.com/?page=sportsbook&group=1000093657&type=live#home','participant--name', 'outcome-value'),
        'nba':('https://mi.betrivers.com/?page=sportsbook&group=1000093652&type=live#home','participant--name', 'outcome-value'),
        'mls':('https://mi.betrivers.com/?page=sportsbook&group=1000095063&type=live#home','participant--name', 'outcome-value'),
    }
)


#must add each additional casino to the below tuple
CASINOS = (fanduel,  betmgm, draftkings, betrivers, betriverslive)

COLUMNS = {'Team 1':[nan],'Max Bet1':[nan],'Max Bet1 Casino':[nan],'Max Bet1 Conv':[nan],'Team 2':[nan],'Max Bet2':[nan],'Max Bet2 Casino':[nan],'Max Bet2 Conv':[nan]}
BASEDF = DataFrame(data=COLUMNS)
COLUMNSDRAW = {'Team 1':[nan],'Max Bet1':[nan],'Max Bet1 Casino':[nan],'Max Bet1 Conv':[nan],'Team 2':[nan],'Max Bet2':[nan],'Max Bet2 Casino':[nan],'Max Bet2 Conv':[nan], 'Max Bet Draw':[nan],'Max Bet Draw Casino':[nan],'Max Bet Draw Conv':[nan]}
BASEDFDRAW = DataFrame(data=COLUMNSDRAW) #base dataframe for sports with 3 outcomes

for casinoindex in range(len(CASINOS)):
    try: #tries for any duplicate columns for casinos that need to use a seperate Casino instance for live games
        BASEDF.insert(1,'Bet1 {}'.format(CASINOS[casinoindex].tag[0]),nan)
        BASEDF.insert(casinoindex+6,'Bet2 {}'.format(CASINOS[casinoindex].tag[0]),nan)
        BASEDFDRAW.insert(1,'Bet1 {}'.format(CASINOS[casinoindex].tag[0]),nan)
        BASEDFDRAW.insert(casinoindex+6,'Bet2 {}'.format(CASINOS[casinoindex].tag[0]),nan)
        BASEDFDRAW.insert((casinoindex*2)+10,'Bet Draw {}'.format(CASINOS[casinoindex].tag[0]),nan)
    except ValueError: #if this casino has already been added it goes to the next casino in the list
        continue

#need to add the sport to the dict below with a copy of its base dataframe "'sport':deepcopy(BASEDF)" or "'sport' = deepcopy(BASEDFDRAW)"
SPORTS = {
    'ufc':deepcopy(BASEDF),
    'mlb':deepcopy(BASEDF),
    'nhl':deepcopy(BASEDF),
    'nba':deepcopy(BASEDF),
    'mls':deepcopy(BASEDFDRAW),
}

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get('https://www.google.com/') #basically initializes the window with this website. All the tabs are then loaded afterwards for easy navigation based on the names
CLASS_NAME = 'class name'

#opening and loading all urls
for casino in CASINOS:
    for sport in usersports:
        try: #Tests if this sport is in this casino. Skips if it is not
            casino.html_data[sport]
        except KeyError:
            print('sport is not implemented for {}'.format(casino.tag[0]))
            continue
        print('Opening ' + casino.tag[0] + ' ' + sport)
        driver.switch_to.new_window(casino.tag[0] + sport)
        driver.get(casino.html_data[sport][0])
        casino.window_handles[sport] = driver.current_window_handle
print('Loading in Web Pages')
sleep(20) #wait time to make sure that all pages are loaded in

#get the data from the urls
for casino in CASINOS:
    for sport in usersports:
        try: #Tests if this sport is in this casino. Skips if it is not
            casino.html_data[sport]
        except KeyError:
            continue
        temp1, temp2 = [], []
        print('Reading in ' + casino.tag[0] + ' ' + sport + ' data')
        #print(driver.current_window_handle) #debug
        #print(casino.window_handles[sport]) #debug
        driver.switch_to.window(casino.window_handles[sport])
        driver_bets = driver.find_elements(By.CLASS_NAME, casino.html_data[sport][2])
        driver_names = driver.find_elements(By.CLASS_NAME, casino.html_data[sport][1])
        for bet in driver_bets:
            temp1.append(bet.text)
        for name in driver_names:
            temp2.append(name.text)
        casino.html_bets[sport] = temp1
        casino.html_names[sport] = temp2
driver.quit()

#sort the data for each casino and sport and create the dataframes for each sport
for casino in CASINOS:
    for sport in usersports:
        try: #Tests if this sport is in this casino. Skips if it is not
            casino.html_data[sport]
        except KeyError:
            continue
        print('Sorting ' + casino.tag[0] + ' ' + sport + ' data')
        # print(html_bets[casino + sport + 'bets']) #debug
        #need to add another elif statement for each new sport
        if sport == 'ufc':
            names1, names2, bets1, bets2 = casino.tag[1].ufc_data(casino.html_names[sport], casino.html_bets[sport])
            SPORTS[sport] = makedf_all(SPORTS[sport], names1, names2, bets1, bets2, casino.tag[0])
        elif sport == 'mlb':
            names1, names2, bets1, bets2 = casino.tag[1].mlb_data(casino.html_names[sport], casino.html_bets[sport])
            SPORTS[sport] = makedf_all(SPORTS[sport], names1, names2, bets1, bets2, casino.tag[0])
        elif sport == 'nba':
            names1, names2, bets1, bets2 = casino.tag[1].nba_data(casino.html_names[sport], casino.html_bets[sport])
            SPORTS[sport] = makedf_all(SPORTS[sport], names1, names2, bets1, bets2, casino.tag[0])
        elif sport == 'nhl':
            names1, names2, bets1, bets2 = casino.tag[1].nhl_data(casino.html_names[sport], casino.html_bets[sport])
            SPORTS[sport] = makedf_all(SPORTS[sport], names1, names2, bets1, bets2, casino.tag[0])
        elif sport == 'mls':
            names1, names2, bets1, bets2, bets3 = casino.tag[1].mls_data(casino.html_names[sport], casino.html_bets[sport])
            SPORTS[sport] = makedf_all3outcome(SPORTS[sport], names1, names2, bets1, bets2, bets3, casino.tag[0])
        else:
            print('Unimplemented Sport') #this should never happen

#calculate the arbs for each sport and generate the spreadsheets
for casino in CASINOS:
    for sport in usersports:
        try: #Tests if this sport is in this casino. Skips if it is not
            casino.html_data[sport]
        except KeyError:
            continue
        print('Calculating ' + casino.tag[0] + ' ' + sport + ' arbs')
        #need to add each additional sport to the relevent if statement
        if sport == 'ufc' or sport == 'mlb' or sport == 'nba' or sport == 'nhl': #for any sport with only Win/Loss
            SPORTS[sport] = arbs(SPORTS[sport],CASINOS)
            opss(SPORTS[sport])
        elif sport == 'mls': #for any sport with Win/Loss/Draw
            SPORTS[sport] = arbs3outcome(SPORTS[sport],CASINOS)
            opss3outcome(SPORTS[sport])
        else:
            print('Unimplemented Sport') #this should never happen

clear() #clears the terminal before printing all of the dataframes

#print all sport data
for sport in usersports:
    SPORTS[sport].drop(0, inplace=True) #removes the first blank row that was used to initialize it
    print(SPORTS[sport])
    # print(SPORTS[sport].loc['Arb'==True]) #only prints the games that have profitable arbs
    # print(SPORTS[sport][['Team 1', 'Max Bet1', 'Max Bet1 Casino', 'Team 2', 'Max Bet2', 'Max Bet2 Casino', 'Arb value']]) #only print relevant columns with profitable arbs
    # print(SPORTS[sport][['Team 1', 'Max Bet1', 'Max Bet1 Casino', 'Team 2', 'Max Bet2', 'Max Bet2 Casino','Max Bet Draw', 'Max Bet Draw Casino', 'Arb value']]) #only print relevant columns with profitable arbs for 3 outcome sports
