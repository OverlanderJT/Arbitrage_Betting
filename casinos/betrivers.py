from functions import alphabetize, singleconvert


def ufc_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    for i in range(len(html_bets)):
        odd = singleconvert(html_bets[i])
        if ',' in html_names[i]:
            lastname = html_names[i].split(', ')[0]
            firstname = html_names[i].split(', ')[1]
            name = firstname + lastname
            name = name.replace(' ', '')
        else:
            name = html_names[i].replace(' ','')
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
        if i % 6 == 2:
            odd = singleconvert(html_bets[i])
            bets1.append(odd)
        elif i % 6 == 3:
            odd = singleconvert(html_bets[i])
            bets2.append(odd)

    for i in range(len(html_names)):
        name = html_names[i].split(' ')[-1]
        if i%2 == 0:
            names1.append(name)
        elif i%2 ==1:
            names2.append(name)
    return alphabetize(names1, names2, bets1, bets2)


def nba_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    for i in range(len(html_bets)):
        if i % 6 == 2:
            odd = singleconvert(html_bets[i])
            bets1.append(odd)
        elif i % 6 == 3:
            odd = singleconvert(html_bets[i])
            bets2.append(odd)

    for i in range(len(html_names)):
        name = html_names[i].split(' ')[-1]
        if i%2 == 0:
            names1.append(name)
        elif i%2 ==1:
            names2.append(name)
    return alphabetize(names1, names2, bets1, bets2)


def mlb_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    for i in range(len(html_bets)):
        if i % 6 == 0:
            odd = singleconvert(html_bets[i])
            bets1.append(odd)
        elif i % 6 == 1:
            odd = singleconvert(html_bets[i])
            bets2.append(odd)

    for i in range(len(html_names)):
        name = html_names[i].split(' ')[-1]
        if i%2 == 0:
            names1.append(name)
        elif i%2 ==1:
            names2.append(name)
    return alphabetize(names1, names2, bets1, bets2)


def mls_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    bets3 = []
    names1 = []
    names2 = []
    for i in range(len(html_bets)):
        if i % 5 == 0:
            odd = singleconvert(html_bets[i])
            bets1.append(odd)
        elif i % 5 == 1:
            odd = singleconvert(html_bets[i])
            bets2.append(odd)
        elif i % 5 == 4:
            odd = singleconvert(html_bets[i])
            bets3.append(odd)

    for i in range(len(html_names)):
        name = html_names[i].split(' ')[-1]
        if i % 3 == 0:
            names1.append(name)
        elif i % 3 == 1:
            names2.append(name)
    return alphabetize(names1, names2, bets1, bets2, bets3)
    
###################################################################

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
    driver.get('https://mi.betrivers.com/?page=sportsbook&group=1000093883&type=prematch#home')
    time.sleep(10)
    height = driver.execute_script("return document.body.scrollHeight")
    loop = True
    while (loop):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if (new_height == height):
            loop = False
        else:
            height = new_height
    driver_bets = driver.find_elements(By.CLASS_NAME, 'outcome-value')
    driver_names = driver.find_elements(By.CLASS_NAME, 'participant--name')
    for bet in driver_bets:
        temp1.append(bet.text)
    for name in driver_names:
        temp2.append(name.text)
    # print(temp1)
    # print(temp2)

    #print(ufc_data(temp2, temp1))
    temp = ufc_data(temp2, temp1)
    for item in temp:
        print(item)
    driver.quit()
