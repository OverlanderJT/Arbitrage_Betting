from functions import alphabetize, singleconvert


def ufc_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    temp_bets = []

    for i in range(len(html_names)):
        name = html_names[i].replace(".","").replace(" ","")
        temp = ""
        for j in range(len(name)-3):
            temp += name[j]
        if i%2 == 0:
            names1.append(temp)
        elif i%2 == 1:
            names2.append(temp)

    for line in html_bets:
        temp_bets.append(line)
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
    
    return alphabetize(names1, names2, bets1, bets2)

def nhl_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    temp_bets = []

    for line in html_bets:
        temp_bets.append(line)
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
    temp_bets = []

    for line in html_bets:
        temp_bets.append(line)
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

def mlb_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    temp_bets = []

    for line in html_bets:
        temp_bets.append(line)
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

def mls_data(html_names:list, html_bets:list) -> list:
    bets1 = []
    bets2 = []
    bets3 = []
    names1 = []
    names2 = []
    temp_bets = []

    for line in html_bets:
        temp_bets.append(line)
    odd = ["err", "err", "err"]

    for item in temp_bets:
        try:
            a = int(item[-1])
            a = -1
        except:
            a = 1
            odd = [-9999, -9999, -9999]
        if (a < 0):
            temp = ''
            b = -1
            for i in range(len(item)):
                if ((item[i] == "+") or (item[i] == "-")):
                    if (b > -1):
                        odd[b] = singleconvert(temp)
                        temp = ''
                    b += 1
                    temp = temp + item[i]
                elif (item[i] == "\n"):
                    if (b == 2):
                        odd[b] = singleconvert(temp)
                        break
                    continue
                else:
                    temp = temp + item[i]
        
        bets1.append(odd[0])
        bets2.append(odd[2])
        bets3.append(odd[1])

    del bets1[0]
    del bets2[0]
    del bets3[0]

    for i in range(len(html_names)):
        name = html_names[i].replace("FC", "").replace("SC", "").replace("CF", "").replace(" ", "").replace("LA", "LosAngeles")
        
        if (i % 2 == 0):
            names1.append(name)
        elif (i % 2 == 1):
            names2.append(name)

    return alphabetize(names1, names2, bets1, bets2, bets3)

##########################################################

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
    driver.get('https://sports.mi.betmgm.com/en/sports/baseball-23/betting/north-america-9/mlb-75')
    time.sleep(5)
    driver_bets = driver.find_elements(By.CLASS_NAME, 'grid-group-container')
    driver_names = driver.find_elements(By.CLASS_NAME, 'participant')
    for bet in driver_bets:
        temp1.append(bet.text)
    for name in driver_names:
        temp2.append(name.text)
    print(temp1)
    print()
    print(temp2)
    print()
    driver.quit()
    print(mlb_data(temp2, temp1))
