from functions import alphabetize, singleconvert

#This might crash if the bet is 'SUS'
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
        for i in range(3, len(split_game)):
            if ((("+" in split_game[i]) or ("-" in split_game[i]) or ("SUS" in split_game[i])) and (("." not in split_game[i]))):
                temp_data.append(split_game[i])
    
    for i in range(len(temp_data)):
        if (i % 6 == 2):
            bets1.append(temp_data[i])
        elif (i % 6 == 5):
            bets2.append(temp_data[i])
    for i in range(len(html_names)):
        split_name = html_names[i].split(" ")
        if (i % 2 == 0):
            names1.append(split_name[-1])
        elif (i % 2 == 1):
            names2.append(split_name[-1])
            
    return alphabetize(names1, names2, bets1, bets2)

#If error, check the spread bet on website. Might not have a .
def nba_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    temp_data = []

    for item in html_bets:
        split_game = item.split("\n")
        for i in range(3, len(split_game)):
            if ((("+" in split_game[i]) or ("-" in split_game[i]) or ("SUS" in split_game[i])) and (("." not in split_game[i]))):
                temp_data.append(split_game[i])
    
    for i in range(len(temp_data)):
        if (i % 6 == 2):
            bets1.append(temp_data[i])
        elif (i % 6 == 5):
            bets2.append(temp_data[i])
    for i in range(len(html_names)):
        split_name = html_names[i].split(" ")
        if (i % 2 == 0):
            names1.append(split_name[-1])
        elif (i % 2 == 1):
            names2.append(split_name[-1])
            
    return alphabetize(names1, names2, bets1, bets2)

def mlb_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    temp_data = []

    for item in html_bets:
        split_game = item.split("\n")
        for i in range(3, len(split_game)):
            if ((("+" in split_game[i]) or ("-" in split_game[i]) or ("SUS" in split_game[i])) and (("." not in split_game[i]))):
                temp_data.append(split_game[i])
    
    for i in range(len(temp_data)):
        if (i % 6 == 2):
            bets1.append(temp_data[i])
        elif (i % 6 == 5):
            bets2.append(temp_data[i])
    for i in range(len(html_names)):
        split_name = html_names[i].split(" ")
        if (i % 2 == 0):
            names1.append(split_name[-1])
        elif (i % 2 == 1):
            names2.append(split_name[-1])
            
    return alphabetize(names1, names2, bets1, bets2)

#This one will probably also break like UFC
def mls_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    bets3 = []
    names1 = []
    names2 = []
    temp_data = []

    for i in range(len(html_bets)):
        temp = html_bets[i].split("\n")
        odd = singleconvert(temp[1])
        name = temp[0].replace(".","").replace(" ","").replace("FC", "").replace("SC", "").replace("CF", "")
        if i%3 == 0:
            bets1.append(odd)
            names1.append(name)
        elif i%3 == 1:
            bets3.append(odd)
        elif i%3 == 2:
            bets2.append(odd)
            names2.append(name)
    return alphabetize(names1, names2, bets1, bets2, bets3)

##############################################

if __name__ == '__main__':
    '''
    ufc
    https://mi.pointsbet.com/sports/mma/UFC
    name: fsu5r7i
    bets: f10krlro.f1a0sb7x.f14nmd6v

    nhl
    https://mi.pointsbet.com/sports/ice-hockey/NHL
    name: fji5frh.fr8jv7a.f1wtz5iq
    bets: f1t29imj.f1yn18fe.f93i66z

    nba
    https://mi.pointsbet.com/sports/basketball/NBA
    name: fji5frh.fr8jv7a.f1wtz5iq
    bets: f1t29imj.f1yn18fe.f93i66z

    mlb
    https://mi.pointsbet.com/sports/baseball/MLB
    name: fji5frh.fr8jv7a.f1wtz5iq
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
    driver.get('https://mi.pointsbet.com/sports/soccer/Major-League-Soccer')
    time.sleep(5)
    driver_bets = driver.find_elements(By.CLASS_NAME, 'f10krlro.f1a0sb7x.f14nmd6v')
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
    temp = mls_data(temp2, temp1)
    #print(temp)
    for item in temp:
        print(len(item))
        print(item)
