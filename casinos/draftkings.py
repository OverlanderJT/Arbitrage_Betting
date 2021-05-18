from functions import alphabetize, singleconvert
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
#import time


def ufc_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []

    temp_names, temp_bets = [], []
    for i in range(len(html_bets)):
        if (i % 2 == 1):
            temp_bets.append(html_bets[i])
    for name in html_names:
        if (name != ''):
            temp_names.append(name)

    for i in range(len(temp_bets)):
        if i % 2 == 0:
            bets1.append(singleconvert(temp_bets[i].replace("\n", "").replace("\t", "")))
            names1.append(
                temp_names[i].replace("\n", "").replace("\t", "").replace(".", "").replace(" ", ""))
        elif i % 2 == 1:
            bets2.append(singleconvert(temp_bets[i].replace("\n", "").replace("\t", "")))
            names2.append(
                temp_names[i].replace("\n", "").replace("\t", "").replace(".", "").replace(" ", ""))
    return alphabetize(names1, names2, bets1, bets2)


def nhl_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    temp_bets = []
    temp_names = []
    a = -1

    for item in html_bets:
        if (("+" in item) or ("-" in item) or (item == "")):
            temp_bets.append(item)
            
    for i in range(len(html_names)):
        temp1 = html_names[i].replace("\n", "").replace("\t", "")
        temp2 = ''
        for j in range(len(temp1)):
            if (temp1[-1 * (j + 1)] == " "):
                break
            else:
                try:
                    a = int(temp1[-1 * (j + 1)])
                except:
                    a = -1
                if (a < 0):
                    temp2 = temp1[-1 * (j + 1)] + temp2
        temp_names.append(temp2)

    for i in range(len(temp_bets)):
        try:
            odd = singleconvert(temp_bets[i])
        except:
            odd = -9999
        if (i % 6 == 2):
            bets1.append(odd)
        elif (i % 6 == 5):
            bets2.append(odd)
            
    for i in range(len(temp_names)):
        if (i % 2 == 0):
            names1.append(temp_names[i])
        elif (i % 2 == 1):
            names2.append(temp_names[i])
            
    return alphabetize(names1, names2, bets1, bets2)


def nba_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    temp_bets = []
    temp_names = []

    for item in html_bets:
        if (("+" in item) or ("-" in item) or (item == "")):
            temp_bets.append(item)

    for i in range(len(html_names)):
        temp1 = html_names[i].replace("\n", "").replace("\t", "")
        temp2 = ''
        for j in range(len(temp1)):
            if (temp1[-1 * (j + 1)] == " "):
                break
            else:
                temp2 = temp1[-1 * (j + 1)] + temp2
        temp_names.append(temp2)

    for i in range(len(temp_bets)):
        try:
            odd = singleconvert(temp_bets[i])
        except:
            odd = -9999
        if (i % 6 == 2):
            bets1.append(odd)
        elif (i % 6 == 5):
            bets2.append(odd)
            
    for i in range(len(temp_names)):
        if (i % 2 == 0):
            names1.append(temp_names[i])
        elif (i % 2 == 1):
            names2.append(temp_names[i])
    
    return alphabetize(names1, names2, bets1, bets2)

#This function might only work in the case of the games happening the same day
#I'm not entirely sure why this one works the way it does, but until it breaks I'm not touching it
def mlb_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    temp_bets = []
    temp_names = []
    a = -1

    for item in html_bets:
        if (("+" in item) or ("-" in item) or (item == "")):
            temp_bets.append(item)
    
    for i in range(len(html_names)):
        temp1 = html_names[i].replace("\n", "").replace("\t", "")
        temp2 = ''
        for j in range(len(temp1)):
            if (temp1[-1 * (j + 1)] == " "):
                break
            else:
                try:
                    a = int(temp1[-1 * (j + 1)])
                except:
                    a = -1
                if (a < 0):
                    temp2 = temp1[-1 * (j + 1)] + temp2
        temp_names.append(temp2)

    for i in range(len(temp_bets)):
        try:
            odd = singleconvert(temp_bets[i])
        except:
            odd = -9999
        if (i % 6 == 2):
            bets1.append(odd)
        elif (i % 6 == 5):
            bets2.append(odd)
            
    for i in range(len(temp_names)):
        if (i % 2 == 0):
            names1.append(temp_names[i])
        elif (i % 2 == 1):
            names2.append(temp_names[i])
            
    return alphabetize(names1, names2, bets1, bets2)

####################################################################
'''
CLASS_NAME = 'class name'
temp1, temp2 = [], []
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get('https://sportsbook.draftkings.com/leagues/baseball/2003?category=game-lines-&subcategory=game')
driver_bets = driver.find_elements(By.CLASS_NAME, 'sportsbook-table__column-row')
driver_names = driver.find_elements(By.CLASS_NAME, 'event-cell__name')
for bet in driver_bets:
    temp1.append(bet.text)
for name in driver_names:
    temp2.append(name.text)
print(temp1)
print()
print(temp2)
print()
driver.quit()
print(mlb_data(temp2, temp1))
'''
