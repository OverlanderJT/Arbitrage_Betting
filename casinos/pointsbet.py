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

##############################################

if __name__ == '__main__':
    '''
    ufc
    https://mi.pointsbet.com/sports/mma/UFC
    name: fsu5r7i
    bets: f10krlro.f1a0sb7x.f14nmd6v
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
    driver.get('https://mi.pointsbet.com/sports/mma/UFC')
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
    #print(nfl_data(temp2, temp1))
    temp = ufc_data(temp2, temp1)
    for item in temp:
        print(len(item))
        print(item)
