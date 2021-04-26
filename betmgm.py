from functions import *
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def ufc_data():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    html_names, html_bets = javaData(driver, "https://sports.mi.betmgm.com/en/sports/mma-45","participant","ms-font-resizer")
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []

    for i in range(len(html_names)):
        name = html_names[i].text.replace(".","").replace(" ","")
        temp = ""
        for j in range(len(name)-3):
            temp += name[j]
        if i%2 == 0:
            names1.append(temp)
        elif i%2 == 1:
            names2.append(temp)
            
    diff = len(html_bets) - len(html_names)
    for i in range(0, len(html_bets)):
        odd = singleconvert(html_bets[i].text)
        if i%2 == 0:
            bets1.append(odd)
        elif i%2 == 1:
            bets2.append(odd)
    driver.quit()
    return names1, names2, bets1, bets2
    #return alphabetize(names1, names2, bets1, bets2)

def nhl_data():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    html_names, html_bets = javaData(driver, "https://sports.mi.betmgm.com/en/sports/ice-hockey-12/betting/north-america-9/nhl-34","participant","ms-font-resizer")
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []

    for i in range(14, len(html_bets)):
        odd = html_bets[i].text
        if (i % 7 == 5):
            odd = singleconvert(odd)
            bets1.append(odd)
        elif (i % 7 == 6):
            odd = singleconvert(odd)
            bets2.append(odd)
    for i in range(2, len(html_names)):
        temp1 = html_names[i].text
        temp2 = ''
        for j in range(len(temp1)):
            if (temp1[-1*(j+1)] == " "):
                break
            else:
                temp2 = temp1[-1*(j+1)] + temp2
        if (i % 2 == 0):
            names1.append(temp2)
        elif (i % 2 == 1):
            names2.append(temp2)
    driver.quit()
    return alphabetize(names1, names2, bets1, bets2)

def nba_data():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    html_names, html_bets = javaData(driver, "https://sports.mi.betmgm.com/en/sports/basketball-7/betting/north-america-9/nba-6004","participant","ms-font-resizer")
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []

    for i in range(14, len(html_bets)):
        odd = html_bets[i].text
        if (i % 7 == 5):
            odd = singleconvert(odd)
            bets1.append(odd)
        elif (i % 7 == 6):
            odd = singleconvert(odd)
            bets2.append(odd)
    for i in range(2, len(html_names)):
        temp1 = html_names[i].text
        temp2 = ''
        for j in range(len(temp1)):
            if (temp1[-1*(j+1)] == " "):
                break
            else:
                temp2 = temp1[-1*(j+1)] + temp2
        if (i % 2 == 0):
            names1.append(temp2)
        elif (i % 2 == 1):
            names2.append(temp2)
    driver.quit()
    return alphabetize(names1, names2, bets1, bets2)

##########################################################

print(ufc_data())
