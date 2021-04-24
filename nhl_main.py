import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd
import functions as func
import numpy as np
import xlsxwriter as xl
from xlsxwriter.utility import xl_rowcol_to_cell

#These are the URLs for draft kings (DK) and fanduel (FD)
print("Grabbing urls . . .")
url_dk = "https://sportsbook.draftkings.com/leagues/hockey/2022?category=game-lines&subcategory=game"
url_fd = "https://sportsbook.fanduel.com/sports/navigation/1550.1/10329.3"
url_bm = "https://sports.mi.betmgm.com/en/sports/ice-hockey-12/betting/north-america-9/nhl-34"

#gathers the fd data
print("Loading in FanDuels data . . .")
options = Options()
options.headless = True
driver_fd = webdriver.Firefox(options=options)
driver_fd.get(url_fd)
driver_fd.execute_script("window.scrollTo(0,document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
time.sleep(45)
html_bets_fd = driver_fd.find_elements_by_class_name("selectionprice")
html_names_fd = driver_fd.find_elements_by_class_name("name")

#gathers the dk data
print("Loading in Draft Kings data . . .")
page_dk = urllib.request.urlopen(url_dk)
soup_dk = BeautifulSoup(page_dk, "html.parser")
html_bets_dk = soup_dk.find_all("span", attrs={"class": "sportsbook-odds american default-color"})
html_names_dk = soup_dk.find_all("span", attrs={"class": "event-cell__name"})

bets1_fd = []
bets2_fd = []
names1_fd = []
names2_fd = []
#makes the fd name and bet arrays for each fighter
for i in range(len(html_bets_fd)):
    odd = html_bets_fd[i].text
    if (i % 6 == 2):
        odd = func.singleconvert(odd)
        bets1_fd.append(odd)
    elif (i % 6 == 3):
        odd = func.singleconvert(odd)
        bets2_fd.append(odd)

for i in range(len(html_names_fd)):
    temp1 = html_names_fd[i].text
    temp2 = ''
    for j in range(len(temp1)):
        if (temp1[-1*(j+1)] == " "):
            break
        else:
            temp2 = temp1[-1*(j+1)] + temp2
    if (i % 2 == 0):
        names1_fd.append(temp2)
    elif (i % 2 == 1):
        names2_fd.append(temp2)
driver_fd.quit()

#gathers the bm data
print("Loading in BetMGM data . . .")
driver_bm = webdriver.Firefox(options=options)
driver_bm.get(url_bm)
driver_bm.execute_script("window.scrollTo(0,document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
time.sleep(2)
html_bets_bm = driver_bm.find_elements_by_tag_name("ms-font-resizer")
html_names_bm = driver_bm.find_elements_by_class_name("participant")

bets1_dk = []
bets2_dk = []
names1_dk = []
names2_dk = []
temp_bets_dk = []
temp_names_dk = []
#makes the dk name and bet arrays for each fighter
for i in range(len(html_bets_dk) - 16):
    if (i % 3 == 2):
        temp_bets_dk.append(html_bets_dk[i].getText().replace("\n", "").replace("\t", ""))
for i in range(len(html_names_dk) - 16): #the -16 changes depending on how many games there are tomorrow
    temp1 = html_names_dk[i].getText().replace("\n", "").replace("\t", "")
    temp2 = ''
    for j in range(len(temp1)):
        if (temp1[-1*(j+1)] == " "):
            break
        else:
            temp2 = temp1[-1*(j+1)] + temp2
    temp_names_dk.append(temp2)

for i in range(len(temp_bets_dk)):
    odd = func.singleconvert(temp_bets_dk[i])
    if (i % 2 == 0):
        bets1_dk.append(odd)
        names1_dk.append(temp_names_dk[i])
    elif (i % 2 == 1):
        bets2_dk.append(odd)
        names2_dk.append(temp_names_dk[i])
        
bets1_bm = []
bets2_bm = []
names1_bm = []
names2_bm = []
#makes the bm name arrays for each fighter
for i in range(14, len(html_bets_bm)):
    odd = html_bets_bm[i].text
    if (i % 7 == 5):
        odd = func.singleconvert(odd)
        bets1_bm.append(odd)
    elif (i % 7 == 6):
        odd = func.singleconvert(odd)
        bets2_bm.append(odd)
for i in range(2, len(html_names_bm)):
    temp1 = html_names_bm[i].text
    temp2 = ''
    for j in range(len(temp1)):
        if (temp1[-1*(j+1)] == " "):
            break
        else:
            temp2 = temp1[-1*(j+1)] + temp2
    if (i % 2 == 0):
        names1_bm.append(temp2)
    elif (i % 2 == 1):
        names2_bm.append(temp2)
driver_bm.quit()

###############################################################################

names1_dk, names2_dk, bets1_dk, bets2_dk = func.alphabetize(names1_dk, names2_dk, bets1_dk, bets2_dk)
names1_fd, names2_fd, bets1_fd, bets2_fd = func.alphabetize(names1_fd, names2_fd, bets1_fd, bets2_fd)
names1_bm, names2_bm, bets1_bm, bets2_bm = func.alphabetize(names1_bm, names2_bm, bets1_bm, bets2_bm)

#initiilizes all of the dfs. These provide the basis for df_all. Need to add 1 per new casino. These lines might be useless
df_dk = pd.DataFrame({'Team 1':names1_dk,'Bet 1':bets1_dk,'Team 2':names2_dk,'Bet 2':bets2_dk})
df_fd = pd.DataFrame({'Team 1':names1_fd,'Bet 1':bets1_fd,'Team 2':names2_fd,'Bet 2':bets2_fd})
df_bm = pd.DataFrame({'Team 1':names1_bm,'Bet 1':bets1_bm,'Team 2':names2_bm,'Bet 2':bets2_bm})
#initilizes df_all. Need to add 2 more columns for every new casino. 'Bet1 [casino]' and 'Bet2 [casino]'
df_all= pd.DataFrame({'Team 1':names1_dk,"Bet1 dk":bets1_dk,"Bet1 fd":np.nan,"Bet1 bm":np.nan,"Max Bet1":np.nan,'Max Bet1 Casino':np.nan,'Max Bet1 Conv':np.nan,"Team 2":names2_dk,"Bet2 dk":bets2_dk,"Bet2 fd":np.nan,"Bet2 bm":np.nan,"Max Bet2":np.nan,'Max Bet2 Casino':np.nan,"Max Bet2 Conv":np.nan,"Arb value":np.nan,"Arb":np.nan})

#print(df_dk)
#print(df_bm)
#print(df_fd)
#need to add one more use of func.makeDf_all per new casino. Changing the inputs as demonstrated
df_all = func.makedf_all(df_all, names1_bm, names2_bm, bets1_bm, bets2_bm, 'bm')
df_all = func.makedf_all(df_all, names1_fd, names2_fd, bets1_fd, bets2_fd, 'fd')
df_all = func.arbs(df_all)
print(df_all.drop(columns=['Bet1 dk','Bet1 fd','Bet1 bm','Bet2 dk','Bet2 fd','Bet2 bm']))

#print(df_all.loc[df_all['Arb'] == True])
func.opss(df_all)
