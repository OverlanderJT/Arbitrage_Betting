from functions import alphabetize, singleconvert
from functions import alphabetize, singleconvert

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

def mls_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    bets3 = []
    names1 = []
    names2 = []
    temp_bets = []
    temp_names = []
    a = -1

    for name in html_names:
        temp_names.append(name.split(" - "))

    for item in html_bets:
        temp = ""
        for i in range(len(item)):
            if ((item[-1 * (i + 1)] == "+") or (item[-1 * (i + 1)] == "-")):
                temp = item[-1 * (i + 1)] + temp
                break
            else:
                try:
                    a = int(item[-1 * (i + 1)])
                    temp = item[-1 * (i + 1)] + temp
                except:
                    temp = -9999
                    break
        temp_bets.append(temp)

    for names in temp_names:
        name1 = names[0].replace("FC", "").replace(".", "").replace("SC", "").replace(" ", "").replace("CF", "")
        name2 = names[1].replace("FC", "").replace(".", "").replace("SC", "").replace(" ", "").replace("CF", "")
        
        names1.append(name1)
        names2.append(name2)
        
    for i in range(len(temp_bets)):
        odd = singleconvert(temp_bets[i])
        if (i % 3 == 0):
            bets1.append(odd)
        elif (i % 3 == 2):
            bets2.append(odd)
        elif (i % 3 == 1):
            bets3.append(odd)
            
    return alphabetize(names1, names2, bets1, bets2, bets3)

####################################################################
if __name__ == '__main__':
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.common.by import By
    import time
        
    CLASS_NAME = 'class name'
    temp1, temp2, temp3 = [], [], []
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get('https://sportsbook.draftkings.com/leagues/soccer/101?category=game-lines&subcategory=money-line-(regular-time)')
    driver_bets = driver.find_elements(By.CLASS_NAME, 'sportsbook-outcome-cell')
    driver_names = driver.find_elements(By.CLASS_NAME, 'sportsbook-event-accordion__title')
    for bet in driver_bets:
        temp1.append(bet.text)
    for name in driver_names:
        temp2.append(name.text)
    #print(temp1)
    #print()
    #print(temp2)
    #print()
    driver.quit()
    print(mls_data(temp2, temp1))
