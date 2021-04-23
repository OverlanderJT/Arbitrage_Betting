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
url_dk = "https://sportsbook.draftkings.com/leagues/mma/2162?category=fight-lines&subcategory=moneyline"
url_fd = "https://sportsbook.fanduel.com/sports/navigation/7287.1/9886.3"
url_bm = "https://sports.mi.betmgm.com/en/sports/mma-45"

#gathers the fd data
print("Loading in FanDuels data . . .")
options = Options()
options.headless = True
driver_fd = webdriver.Firefox(options=options)
driver_fd.get(url_fd)
driver_fd.execute_script("window.scrollTo(0,document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
time.sleep(15)
html_bets_fd = driver_fd.find_elements_by_class_name("selectionprice")
html_names_fd = driver_fd.find_elements_by_class_name("selection-name")

#gathers the dk data
print("Loading in Draft Kings data . . .")
page_dk = urllib.request.urlopen(url_dk)
soup_dk = BeautifulSoup(page_dk, "html.parser")
html_bets_dk = soup_dk.find_all("span", attrs={"class": "sportsbook-odds american default-color"})
html_names_dk = soup_dk.find_all("span", attrs={"class": "sportsbook-outcome-cell__label"})

bets1_fd = []
bets2_fd = []
names1_fd = []
names2_fd = []
#makes the fd name and bet arrays for each fighter
for i in range(len(html_bets_fd)):
    odd = func.singleconvert(html_bets_fd[i].text)
    name = html_names_fd[i].text.replace(".","").replace(" ","")
    if i%2 == 0:
        bets1_fd.append(odd)
        names1_fd.append(name)
    elif i%2 ==1:
        bets2_fd.append(odd)
        names2_fd.append(name)
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
#makes the dk name and bet arrays for each fighter
for i in range(len(html_bets_dk)):
    if i%2 == 0:
        bets1_dk.append(func.singleconvert(html_bets_dk[i].getText().replace("\n","").replace("\t","")))
        #bets1_dk.append(html_bets_dk[i].getText().replace("\n","").replace("\t",""))
        names1_dk.append(html_names_dk[i].getText().replace("\n","").replace("\t","").replace(".","").replace(" ",""))
    elif i%2 == 1:
        bets2_dk.append(func.singleconvert(html_bets_dk[i].getText().replace("\n", "").replace("\t", "")))
        #bets2_dk.append(html_bets_dk[i].getText().replace("\n", "").replace("\t", ""))
        names2_dk.append(html_names_dk[i].getText().replace("\n", "").replace("\t", "").replace(".","").replace(" ",""))

bets1_bm = []
bets2_bm = []
names1_bm = []
names2_bm = []
#makes the bm name arrays for each fighter
for i in range(len(html_names_bm)):
    name = html_names_bm[i].text.replace(".","").replace(" ","")
    temp = ""
    for j in range(len(name)-3):
        temp += name[j]
    if i%2 == 0:
        names1_bm.append(temp)
    elif i%2 == 1:
        names2_bm.append(temp)
#makes the bm bet arrays for each fighter
diff = len(html_bets_bm) - len(html_names_bm)
for i in range(diff, len(html_bets_bm)):
    odd = func.singleconvert(html_bets_bm[i].text)
    #odd = html_bets_bm[i].text
    if i%2 == 0:
        bets1_bm.append(odd)
    elif i%2 == 1:
        bets2_bm.append(odd)
driver_bm.quit()

###############################################################################

names1_dk, names2_dk, bets1_dk, bets2_dk = func.alphabetize(names1_dk, names2_dk, bets1_dk, bets2_dk)
names1_fd, names2_fd, bets1_fd, bets2_fd = func.alphabetize(names1_fd, names2_fd, bets1_fd, bets2_fd)
names1_bm, names2_bm, bets1_bm, bets2_bm = func.alphabetize(names1_bm, names2_bm, bets1_bm, bets2_bm)

#initiilizes all of the dfs. These provide the basis for df_all. Need to add 1 per new casino
df_dk = pd.DataFrame({'Team 1':names1_dk,'Bet 1':bets1_dk,'Team 2':names2_dk,'Bet 2':bets2_dk})
df_fd = pd.DataFrame({'Team 1':names1_fd,'Bet 1':bets1_fd,'Team 2':names2_fd,'Bet 2':bets2_fd})
df_bm = pd.DataFrame({'Team 1':names1_bm,'Bet 1':bets1_bm,'Team 2':names2_bm,'Bet 2':bets2_bm})
#initilizes df_all. Need to add 2 more columns for every new casino. 'Bet1 [casino]' and 'Bet2 [casino]'
df_all= pd.DataFrame({'Team 1':names1_dk,"Bet1 dk":bets1_dk,"Bet1 fd":np.nan,"Bet1 bm":np.nan,"Max Bet1":np.nan,"Max Bet1 Casino":np.nan,'Max Bet1 Conv':np.nan,"Team 2":names2_dk,"Bet2 dk":bets2_dk,"Bet2 fd":np.nan,"Bet2 bm":np.nan,"Max Bet2":np.nan,"Max Bet2 Casino":np.nan,"Max Bet2 Conv":np.nan,"Arb value":np.nan,"Arb":np.nan})
'''
print(df_dk)
print(df_bm)
print(df_fd)
'''
#need to add one more use of func.makeDf_all per new casino. Changing the inputs as demonstrated
df_all = func.makedf_all(df_all, names1_bm, names2_bm, bets1_bm, bets2_bm, 'bm')
df_all = func.makedf_all(df_all, names1_fd, names2_fd, bets1_fd, bets2_fd, 'fd')
df_all = func.arbs(df_all)

print(df_all.drop(columns=['Bet1 dk','Bet1 fd','Bet1 bm','Bet2 dk','Bet2 fd','Bet2 bm']))
#print(len(names1_fd))
#print(df_all.loc[df_all['Arb'] == True])
#tempDf = pd.DataFrame()
#tempDf = tempDf.append({'Team 1':'Bob','Max Bet1 Casino':'fd','Max Bet1 Conv':2.5,'Team 2':'Jimmy','Max Bet2 Casino':'dk','Max Bet2 Conv':3,'Arb':True}, ignore_index=True)
#func.opss(tempDf)
func.opss(df_all)
