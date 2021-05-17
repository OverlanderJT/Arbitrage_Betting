from functions import alphabetize, singleconvert
#from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.common.by import By
#import time


def ufc_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []

    for i in range(len(html_bets)):
        if i % 2 == 0:
            bets1.append(singleconvert(html_bets[i].replace("\n", "").replace("\t", "")))
            names1.append(
                html_names[i].replace("\n", "").replace("\t", "").replace(".", "").replace(" ", ""))
        elif i % 2 == 1:
            bets2.append(singleconvert(html_bets[i].replace("\n", "").replace("\t", "")))
            names2.append(
                html_names[i].replace("\n", "").replace("\t", "").replace(".", "").replace(" ", ""))
    return alphabetize(names1, names2, bets1, bets2)


def nhl_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    temp_bets = []
    temp_names = []
    a = -1

    for i in range(len(html_bets)):
        if (i % 3 == 2):
            temp_bets.append(html_bets[i].replace("\n", "").replace("\t", ""))
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
        odd = singleconvert(temp_bets[i])
        if (i % 2 == 0):
            bets1.append(odd)
            names1.append(temp_names[i])
        elif (i % 2 == 1):
            bets2.append(odd)
            names2.append(temp_names[i])
            
    return alphabetize(names1, names2, bets1, bets2)


def nba_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    temp_bets = []
    temp_names = []

    for i in range(len(html_bets)): #for some reason names1 and names2 are different lengths
        if (i % 3 == 2):
            temp_bets.append(html_bets[i].replace("\n", "").replace("\t", ""))
    for i in range(len(html_names)):
        temp1 = html_names[i].replace("\n", "").replace("\t", "")
        temp2 = ''
        for j in range(len(temp1)):
            if (temp1[-1 * (j + 1)] == " "):
                break
            else:
                temp2 = temp1[-1 * (j + 1)] + temp2
        temp_names.append(temp2)

    for i in range(len(temp_bets)): #since temp_bets is too short for some reason (11 as of writing this comment)
        odd = singleconvert(temp_bets[i]) #the names and bets arrays are messed up. temp_names is 14 long
        if (i % 2 == 0):
            bets1.append(odd)
            names1.append(temp_names[i])
        elif (i % 2 == 1):
            bets2.append(odd)
            names2.append(temp_names[i])
    return alphabetize(names1, names2, bets1, bets2)

#This function might only work in the case of the games happening the same day
#I'm not entirely sure why this one works the way it does, but I'll touch it later
def mlb_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    temp_bets = []
    temp_names = []
    a = -1

    for i in range(len(html_bets)):
        if (i % 3 == 2):
            temp_bets.append(html_bets[i].replace("\n", "").replace("\t", ""))
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
        odd = singleconvert(temp_bets[i])
        if (i % 2 == 0):
            bets1.append(odd)
            names1.append(temp_names[i])
        elif (i % 2 == 1):
            bets2.append(odd)
            names2.append(temp_names[i])
            
    return alphabetize(names1, names2, bets1, bets2)

####################################################################

'''
CLASS_NAME = 'class name'
temp1, temp2 = [], []
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get('https://sportsbook.draftkings.com/leagues/basketball/103?category=game-lines&subcategory=game')
driver_bets = driver.find_elements(By.CLASS_NAME, 'sportsbook-outcome-cell__element')
driver_names = driver.find_elements(By.CLASS_NAME, 'event-cell__name')
print(driver_bets)
for bet in driver_bets:
    temp1.append(bet.text)
for name in driver_names:
    temp2.append(name.text)
print(temp1)
print(temp2)
driver.quit()
'''
