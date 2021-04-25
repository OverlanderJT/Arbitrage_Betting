from functions import *


def ufc_data():
    html_names,html_bets = data("https://sportsbook.draftkings.com/leagues/mma/2162?category=fight-lines&subcategory=moneyline","span","sportsbook-outcome-cell__label","span","sportsbook-odds american default-color")
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []

    for i in range(len(html_bets)):
        if i % 2 == 0:
            bets1.append(singleconvert(html_bets[i].getText().replace("\n", "").replace("\t", "")))
            names1.append(
                html_names[i].getText().replace("\n", "").replace("\t", "").replace(".", "").replace(" ", ""))
        elif i % 2 == 1:
            bets2.append(singleconvert(html_bets[i].getText().replace("\n", "").replace("\t", "")))
            names2.append(
                html_names[i].getText().replace("\n", "").replace("\t", "").replace(".", "").replace(" ", ""))
    return alphabetize(names1, names2, bets1, bets2)


def nhl_data():
    html_names, html_bets = data("https://sportsbook.draftkings.com/leagues/hockey/2022?category=game-lines&subcategory=game", "span","event-cell__name", "span", "sportsbook-odds american default-color")
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    temp_bets = []
    temp_names = []

    for i in range(len(html_bets) - 16):
        if (i % 3 == 2):
            temp_bets.append(html_bets[i].getText().replace("\n", "").replace("\t", ""))
    for i in range(len(html_names) - 16):  # the -16 changes depending on how many games there are tomorrow
        temp1 = html_names[i].getText().replace("\n", "").replace("\t", "")
        temp2 = ''
        for j in range(len(temp1)):
            if (temp1[-1 * (j + 1)] == " "):
                break
            else:
                temp2 = temp1[-1 * (j + 1)] + temp2
        temp_names.append(temp2)

    for i in range(len(temp_bets)):
        odd = singleconvert(temp_bets[i])
        if (i % 2 == 0):
            bets1.append(odd)
            names1.append(temp_names[i])
        elif (i % 2 == 1):
            bets2.append(odd)
            names2.append(temp_names[i])
    return alphabetize(names1, names2, bets1, bets2)


def nba_data():
    html_names, html_bets = data("https://sportsbook.draftkings.com/leagues/basketball/103?category=game-lines&subcategory=game", "span","event-cell__name", "span", "sportsbook-odds american default-color")
    bets1 = []
    bets2 = []
    names1 = []
    names2 = []
    temp_bets = []
    temp_names = []

    for i in range(len(html_bets)): #for some reason names1 and names2 are different lengths
        if (i % 3 == 2):
            temp_bets.append(html_bets[i].getText().replace("\n", "").replace("\t", ""))
    for i in range(len(html_names)):
        temp1 = html_names[i].getText().replace("\n", "").replace("\t", "")
        temp2 = ''
        for j in range(len(temp1)):
            if (temp1[-1 * (j + 1)] == " "):
                break
            else:
                temp2 = temp1[-1 * (j + 1)] + temp2
        temp_names.append(temp2)

    for i in range(len(temp_bets)):
        odd = singleconvert(temp_bets[i])
        if (i % 2 == 0):
            bets1.append(odd)
            names1.append(temp_names[i])
        elif (i % 2 == 1):
            bets2.append(odd)
            names2.append(temp_names[i])
    print(len(names1))
    print(len(names2))
    return alphabetize(names1, names2, bets1, bets2)

####################################################################

print(nba_data())
