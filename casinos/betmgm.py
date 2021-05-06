from functions import *
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def ufc_data():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    html_names, html_bets = javaData(driver, "https://sports.mi.betmgm.com/en/sports/mma-45","participant","grid-group-container")
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    temp_bets = []

    for i in range(len(html_names)):
        name = html_names[i].text.replace(".","").replace(" ","")
        temp = ""
        for j in range(len(name)-3):
            temp += name[j]
        if i%2 == 0:
            names1.append(temp)
        elif i%2 == 1:
            names2.append(temp)

    for line in html_bets:
        temp_bets.append(line.text)
    odd1 = "err"
    odd2 = "err"

    for item in temp_bets:
        try:
            a = int(item[-1])
            a = -1
        except:
            a = 1
            odd1 = -9999
            odd2 = -9999
        if (a < 0):
            temp = ''
            b = 0
            for i in range(len(item)):
                if (item[-1 * (i + 1)] == '\n'):
                    odd2 = singleconvert(temp)
                    temp = ''
                    i += 1
                elif ((item[-1 * (i + 1)] == '+') or (item[-1 * (i + 1)] == '-')):
                    b += 1
                    temp = item[-1 * (i + 1)] + temp
                    if (b == 2):
                        odd1 = singleconvert(temp)
                        break
                elif (item[-1 * (i + 1)] == '.'):
                    odd1 = -9999
                    odd2 = -9999
                    break
                else:
                    temp = item[-1 * (i + 1)] + temp
        bets1.append(odd1)
        bets2.append(odd2)

    del bets1[0]
    del bets2[0]
    
    driver.quit()
    return alphabetize(names1, names2, bets1, bets2)

def nhl_data():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    html_names, html_bets = javaData(driver, "https://sports.mi.betmgm.com/en/sports/ice-hockey-12/betting/north-america-9/nhl-34","participant","grid-group-container")
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    temp_bets = []

    for line in html_bets:
        temp_bets.append(line.text)
    odd1 = "err"
    odd2 = "err"

    for item in temp_bets:
        try:
            a = int(item[-1])
            a = -1
        except:
            a = 1
            odd1 = -9999
            odd2 = -9999
        if (a < 0):
            temp = ''
            b = 0
            for i in range(len(item)):
                if (item[-1 * (i + 1)] == '\n'):
                    odd2 = singleconvert(temp)
                    temp = ''
                    i += 1
                elif ((item[-1 * (i + 1)] == '+') or (item[-1 * (i + 1)] == '-')):
                    b += 1
                    temp = item[-1 * (i + 1)] + temp
                    if (b == 2):
                        odd1 = singleconvert(temp)
                        break
                elif (item[-1 * (i + 1)] == '.'):
                    odd1 = -9999
                    odd2 = -9999
                    break
                else:
                    temp = item[-1 * (i + 1)] + temp
        bets1.append(odd1)
        bets2.append(odd2)

    del bets1[0]
    del bets2[0]
            
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
    html_names, html_bets = javaData(driver, "https://sports.mi.betmgm.com/en/sports/basketball-7/betting/north-america-9/nba-6004","participant","grid-group-container")
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    temp_bets = []

    for line in html_bets:
        temp_bets.append(line.text)
    odd1 = "err"
    odd2 = "err"

    for item in temp_bets:
        try:
            a = int(item[-1])
            a = -1
        except:
            a = 1
            odd1 = -9999
            odd2 = -9999
        if (a < 0):
            temp = ''
            b = 0
            for i in range(len(item)):
                if (item[-1 * (i + 1)] == '\n'):
                    odd2 = singleconvert(temp)
                    temp = ''
                    i += 1
                elif ((item[-1 * (i + 1)] == '+') or (item[-1 * (i + 1)] == '-')):
                    b += 1
                    temp = item[-1 * (i + 1)] + temp
                    if (b == 2):
                        odd1 = singleconvert(temp)
                        break
                elif (item[-1 * (i + 1)] == '.'):
                    odd1 = -9999
                    odd2 = -9999
                    break
                else:
                    temp = item[-1 * (i + 1)] + temp
        bets1.append(odd1)
        bets2.append(odd2)

    del bets1[0]
    del bets2[0]

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

def mlb_data():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    html_names, html_bets = javaData(driver, "https://sports.mi.betmgm.com/en/sports/baseball-23/betting/north-america-9/mlb-75","participant","grid-group-container")
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    temp_bets = []

    for line in html_bets:
        temp_bets.append(line.text)
    odd1 = "err"
    odd2 = "err"

    for item in temp_bets:
        try:
            a = int(item[-1])
            a = -1
        except:
            a = 1
            odd1 = -9999
            odd2 = -9999
        if (a < 0):
            temp = ''
            b = 0
            for i in range(len(item)):
                if (item[-1 * (i + 1)] == '\n'):
                    odd2 = singleconvert(temp)
                    temp = ''
                    i += 1
                elif ((item[-1 * (i + 1)] == '+') or (item[-1 * (i + 1)] == '-')):
                    b += 1
                    temp = item[-1 * (i + 1)] + temp
                    if (b == 2):
                        odd1 = singleconvert(temp)
                        break
                elif (item[-1 * (i + 1)] == '.'):
                    odd1 = -9999
                    odd2 = -9999
                    break
                else:
                    temp = item[-1 * (i + 1)] + temp
        bets1.append(odd1)
        bets2.append(odd2)

    del bets1[0]
    del bets2[0]
    #If a line error goes wrong, it's probably because of the two lines directly below
    #They are needed at time of writing, but not sure if they're important forever
    del bets1[-1]
    del bets2[-1]

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

