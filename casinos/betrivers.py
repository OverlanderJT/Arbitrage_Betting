from functions import alphabetize, singleconvert


def ufc_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    for i in range(len(html_bets)):
        print(i)
        odd = singleconvert(html_bets[i])
        name = html_names[i].replace(' ','')
        if ',' in html_names[i]:
            lastname = html_names[i].split(',')[0]
            firstname = html_names[i].split(',')[1]
            name = firstname + lastname
        if i%2 == 0:
            bets1.append(odd)
            names1.append(name)
        elif i%2 ==1:
            bets2.append(odd)
            names2.append(name)
    return alphabetize(names1, names2, bets1, bets2)


def nhl_data(html_names:list, html_bets:list) -> list:
    pass


def nba_data(html_names:list, html_bets:list) -> list:
    pass


def mlb_data(html_names:list, html_bets:list) -> list:
    pass


def mls_data(html_names:list, html_bets:list) -> list:
    pass
    

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
    driver.get('https://mi.betrivers.com/?page=sportsbook&group=1000093657&type=prematch#home')
    time.sleep(10)
    driver_bets = driver.find_elements(By.CLASS_NAME, 'outcome-value')
    driver_names = driver.find_elements(By.CLASS_NAME, 'participant--name')
    for bet in driver_bets:
        temp1.append(bet.text)
    for name in driver_names:
        temp2.append(name.text)
    print(len(temp1))
    print(len(temp2))
    print(temp1)
    print(temp2)

    # print(nhl_data(temp2, temp1))
