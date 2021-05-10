from functions import *


def ufc_data(html_names, html_bets):
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    
    for i in range(len(html_bets)):
        odd = singleconvert(html_bets[i].text)
        name = html_names[i].text.replace(".","").replace(" ","")
        if i%2 == 0:
            bets1.append(odd)
            names1.append(name)
        elif i%2 ==1:
            bets2.append(odd)
            names2.append(name)
    return alphabetize(names1, names2, bets1, bets2)


def nhl_data(html_names, html_bets):
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []

    for i in range(len(html_bets)):
        odd = html_bets[i].text
        if (i % 6 == 2):
            odd = singleconvert(odd)
            bets1.append(odd)
        elif (i % 6 == 3):
            odd = singleconvert(odd)
            bets2.append(odd)

    for i in range(len(html_names)):
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
    return alphabetize(names1, names2, bets1, bets2)


def nba_data(html_names, html_bets):
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []

    for i in range(len(html_bets)):
        odd = html_bets[i].text
        if (i % 6 == 2):
            odd = singleconvert(odd)
            bets1.append(odd)
        elif (i % 6 == 3):
            odd = singleconvert(odd)
            bets2.append(odd)

    for i in range(len(html_names)):
        temp1 = html_names[i].text
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

def mlb_data(html_names, html_bets):
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []

    for i in range(len(html_bets)):
        odd = html_bets[i].text
        if (i % 6 == 2):
            odd = singleconvert(odd)
            bets1.append(odd)
        elif (i % 6 == 3):
            odd = singleconvert(odd)
            bets2.append(odd)

    for i in range(len(html_names)):
        temp1 = html_names[i].text
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
    
##############################################


