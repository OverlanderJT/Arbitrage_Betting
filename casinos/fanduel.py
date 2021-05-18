from functions import alphabetize, singleconvert
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

def ufc_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    
    for i in range(len(html_bets)):
        odd = singleconvert(html_bets[i])
        name = html_names[i].replace(".","").replace(" ","")
        if i%2 == 0:
            bets1.append(odd)
            names1.append(name)
        elif i%2 ==1:
            bets2.append(odd)
            names2.append(name)
    return alphabetize(names1, names2, bets1, bets2)


def nhl_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []

    for i in range(len(html_bets)):
        odd = html_bets[i]
        if (i % 6 == 2):
            odd = singleconvert(odd)
            bets1.append(odd)
        elif (i % 6 == 3):
            odd = singleconvert(odd)
            bets2.append(odd)

    for i in range(len(html_names)):
        temp1 = html_names[i]
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
    return alphabetize(names1, names2, bets1, bets2)


def nba_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []

    for i in range(len(html_bets)):
        odd = html_bets[i]
        if (i % 6 == 2):
            odd = singleconvert(odd)
            bets1.append(odd)
        elif (i % 6 == 3):
            odd = singleconvert(odd)
            bets2.append(odd)

    for i in range(len(html_names)):
        temp1 = html_names[i]
        temp2 = ''
        for j in range(len(temp1)):
            if (temp1[-1 * (j + 1)] == " "):
                break
            else:
                temp2 = temp1[-1 * (j + 1)] + temp2
        if (i % 2 == 0):
            names1.append(temp2)
        elif (i % 2 == 1):
            names2.append(temp2)
    return alphabetize(names1, names2, bets1, bets2)

def mlb_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []

    for i in range(len(html_bets)):
        odd = html_bets[i]
        if (i % 6 == 2):
            odd = singleconvert(odd)
            bets1.append(odd)
        elif (i % 6 == 3):
            odd = singleconvert(odd)
            bets2.append(odd)

    for i in range(len(html_names)):
        temp1 = html_names[i]
        temp2 = ''
        for j in range(len(temp1)):
            if (temp1[-1 * (j + 1)] == " "):
                break
            else:
                temp2 = temp1[-1 * (j + 1)] + temp2
        if (i % 2 == 0):
            names1.append(temp2)
        elif (i % 2 == 1):
            names2.append(temp2)
    return alphabetize(names1, names2, bets1, bets2)

def mls_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    bets3 = []
    names1 = []
    names2 = []

    for i in range(len(html_bets)):
        odd = html_bets[i]
        odd = singleconvert(odd)
        if (i % 3 == 0):
            bets1.append(odd)
        elif (i % 3 == 2):
            bets2.append(odd)
        elif (i % 3 == 1):
            bets3.append(odd)

    for i in range(len(html_names)):
        temp = html_names[i]
        if (i % 2 == 0):
            names1.append(temp)
        elif (i % 2 == 1):
            names2.append(temp)
    return alphabetize(names1, names2, bets1, bets2, bets3)

##############################################

if __name__ == '__main__':
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.common.by import By
    import time
    
    CLASS_NAME = 'class name'
    temp1, temp2 = [], []
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get('https://sportsbook.fanduel.com/sports/navigation/730.1/9507.1')
    time.sleep(5)
    driver_bets = driver.find_elements(By.CLASS_NAME, 'sh')
    driver_names = driver.find_elements(By.CLASS_NAME, 'name')
    for bet in driver_bets:
        temp1.append(bet.text)
    for name in driver_names:
        temp2.append(name.text)
    print(temp1)
    print()
    print(temp2)
    print()
    driver.quit()
    print(mls_data(temp2, temp1))
