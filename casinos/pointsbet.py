from functions import alphabetize, singleconvert

def ufc_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    
    for i in range(len(html_bets)):
        temp = html_bets[i].split("\n")
        odd = singleconvert(temp[1])
        name = temp[0].replace(".","").replace(" ","")
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
    temp_data = []

    for item in html_bets:
        split_game = item.split("\n")
        a = 1
        for i in range(3, len(split_game)):
            if (("." in split_game[i]) or ("Ov " in split_game[i]) or ("Un " in split_game[i])):
                a = -2

            if (a >= 0):
                temp_data.append(split_game[i])
            a += 1
        name1 = temp_data[0].split(" ")
        name2 = temp_data[2].split(" ")
        try:
            names1.append(name1[-1])
            bets1.append(temp_data[1])
            names2.append(name2[-1])
            bets2.append(temp_data[3])
        except:
            pass
        temp_data = []

    return alphabetize(names1, names2, bets1, bets2)

##############################################

if __name__ == '__main__':
    '''
    ufc
    https://mi.pointsbet.com/sports/mma/UFC
    name: fsu5r7i
    bets: f10krlro.f1a0sb7x.f14nmd6v

    nhl
    https://mi.pointsbet.com/sports/ice-hockey/NHL
    name: fsu5r7i
    bets: f1t29imj.f1yn18fe.f93i66z
    '''
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.common.by import By
    import time
    
    CLASS_NAME = 'class name'
    temp1, temp2 = [], []
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get('https://mi.pointsbet.com/sports/ice-hockey/NHL')
    time.sleep(5)
    driver_bets = driver.find_elements(By.CLASS_NAME, 'f1t29imj.f1yn18fe.f93i66z')
    driver_names = driver.find_elements(By.CLASS_NAME, 'fsu5r7i')
    for bet in driver_bets:
        temp1.append(bet.text)
    for name in driver_names:
        temp2.append(name.text)
    print(temp1)
    print()
    print(temp2)
    print()
    driver.quit()
    temp = nhl_data(temp2, temp1)
    for item in temp:
        print(len(item))
        print(item)
