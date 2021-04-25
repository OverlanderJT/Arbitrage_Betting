import numpy as np
import xlsxwriter as xl
from xlsxwriter.utility import xl_rowcol_to_cell
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time


class Casino():
    nbaname = ''
    nbabet = ''
    ufcname = ''
    ufcbet = ''
    nhlname = ''
    nhlbet = ''

    def __init__(self,id,ufcurl,nbaurl,mlburl,nhlurl,):
        self.id = id
        self.ufcurl = ufcurl
        self.nbaurl = nbaurl
        self.mlburl = mlburl
        self.nhlurl = nhlurl


def javaData(driver, url, nameclass, betclass):
    driver.get(url)
    driver.execute_script(
        "window.scrollTo(0,document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(5)
    html_bets = driver.find_elements_by_class_name(betclass)
    html_names = driver.find_elements_by_class_name(nameclass)
    return html_names, html_bets

def data(url, nametag, nameclass, bettag, betclass):
    page_dk = urllib.request.urlopen(url)
    soup_dk = BeautifulSoup(page_dk, "html.parser")
    html_bets = soup_dk.find_all(bettag, attrs={"class": betclass})
    html_names = soup_dk.find_all(nametag, attrs={"class": nameclass})
    return html_names,html_bets


def alphabetize(names1, names2, bets1, bets2):
    #rearranges the fighters so that the first and second names are in alphabetical order
    for i in range(len(names1)):
        tempName = names1[i]
        tempBet = bets1[i]
        if names1[i] > names2[i]:
            names1[i] = names2[i]
            names2[i] = tempName
            bets1[i] = bets2[i]
            bets2[i] = tempBet
    return names1, names2, bets1, bets2

def singleconvert(odd):
    #converts the data from string to the converted odds for future calcs
    conv = int(odd.replace("+", ""))
    return conv

def makedf_all(df, names1, names2, bets1, bets2, casino, casinolist):
    #adds all of the fights to the final df, combining when it can

    for i in casinolist:
        if casino == i:
            bet1 = 'Bet1 {}'.format(i)
            bet2 = 'Bet2 {}'.format(i)

    #compares the df_all to the new df being added. If the fight names match, adds the bets, if not, adds the new fight to the end of the df.
    #this makes it so that this can be used for an infinite amount of casinos (assuming the relavent columns have been added)
    for i in range(len(names1)):
        for j in range(len(df.index)):
            if df.at[j,'Team 1'] == names1[i] and df.at[j,'Team 2'] == names2[i]:
                df.at[j, bet1] = bets1[i]
                df.at[j, bet2] = bets2[i]
                break
            if j == len(df.index)-1:
                df = df.append({'Team 1': names1[i], bet1: bets1[i], 'Team 2': names2[i], bet2: bets2[i]},ignore_index=True)
    return df

def arbs(df, casinolist):
    #finds the max bets
    df['Max Bet1'] = df.iloc[:,1:len(casinolist)+1].max(axis=1)
    df['Max Bet1 Casino'] = df.iloc[:,1:len(casinolist)+1].idxmax(axis='columns').str[-2:]

    df['Max Bet2'] = df.iloc[:,(5+len(casinolist)):len(casinolist)+(5+len(casinolist))].max(axis=1)
    df['Max Bet2 Casino'] = df.iloc[:,(5+len(casinolist)):len(casinolist)+(5+len(casinolist))].idxmax(axis='columns').str[-2:]

    #converts max bets to non american odds
    df.loc[df['Max Bet1'] < 0, 'Max Bet1 Conv'] = (-100 / df['Max Bet1']) + 1
    df.loc[df['Max Bet1'] > 0, 'Max Bet1 Conv'] = (df['Max Bet1'] / 100) + 1
    df.loc[df['Max Bet2'] < 0, 'Max Bet2 Conv'] = (-100 / df['Max Bet2']) + 1
    df.loc[df['Max Bet2'] > 0, 'Max Bet2 Conv'] = (df['Max Bet2'] / 100) + 1

    #calculates arbs and fill NaN values
    df['Arb value'] = (1 / df['Max Bet1 Conv']) + (1 / df['Max Bet2 Conv'])
    df.loc[df['Arb value'] <= 1, 'Arb'] = True
    df = df.fillna(value={'Arb':False})
    df = df.fillna(0)

    return df

def opss(df):
    #output spreadsheet for all viable arbs
    tempdf = pd.DataFrame()
    tempdf = tempdf.append(df.loc[df['Arb'] == True], ignore_index=True)
    for i in range(len(df['Max Bet1 Conv'].loc[df['Arb'] == True].index)): #might be able to get rid of the 'Max Bet1' part

        wb = xl.Workbook(tempdf.at[i,'Team 1'] + ' vs ' + tempdf.at[i,'Team 2'] + '.xlsx')
        sheet1 = wb.add_worksheet()
        sheet2 = wb.add_worksheet()
        sheet3 = wb.add_worksheet()

        # adding the formats used throughout the wb
        bold = wb.add_format({'bold': True})
        red_format = wb.add_format({'font_color': '#9C0006', 'bg_color': '#FFC7CE'})
        green_format = wb.add_format({'font_color': '#006100', 'bg_color': '#C6EFCE'})
        yellow_format = wb.add_format({'font_color': '#9C5700', 'bg_color': '#FFEB9C'})

        sheet1.write('B1', tempdf.at[i,'Team 1'], bold)
        sheet1.write('B2', tempdf.at[i,'Max Bet1 Conv'])
        sheet1.write('B3', tempdf.at[i,'Max Bet1 Casino'])
        sheet1.write('C1', tempdf.at[i,'Team 2'], bold)
        sheet1.write('C2', tempdf.at[i,'Max Bet2 Conv'])
        sheet1.write('C3', tempdf.at[i,'Max Bet2 Casino'])

        sheet1.write('E1', 'Arb', bold)
        sheet1.write_formula('E2', '=(1/B2) + (1/C2)')
        sheet1.conditional_format('E2', {'type': 'cell', 'criteria': 'greater than', 'value': 1, 'format': red_format})
        sheet1.conditional_format('E2', {'type': 'cell', 'criteria': 'between', 'minimum': 0.95, 'maximum': 1,'format': green_format})
        sheet1.conditional_format('E2', {'type': 'cell', 'criteria': 'less than', 'value': 0.95, 'format': yellow_format})
        sheet2.conditional_format('B2:U21', {'type': 'cell', 'criteria': '>=', 'value': 1, 'format': green_format})
        sheet3.conditional_format('B2:U21', {'type': 'cell', 'criteria': '>=', 'value': 1, 'format': green_format})
        sheet1.conditional_format('C6:V25', {'type': 'cell', 'criteria': '>=', 'value': 1, 'format': green_format})

        sheet1.write('B5', 'b, a', bold)
        sheet2.write('A1', 'a', bold)
        sheet3.write('A1', 'b', bold)

        for k in range(20):  # row
            # add a and b values for each sheet
            sheet1.write(4, 2 + k, k + 1, bold)
            sheet1.write(5 + k, 1, k + 1, bold)
            sheet2.write(0, k + 1, k + 1, bold)
            sheet2.write(k + 1, 0, k + 1, bold)
            sheet3.write(0, k + 1, k + 1, bold)
            sheet3.write(k + 1, 0, k + 1, bold)

            for j in range(20):  # column
                sheet1.write_formula(k + 5, j + 2,'=IF(AND(Sheet2!{}>=1, Sheet3!{}>=1),1,0)'.format(xl_rowcol_to_cell(k + 1, j + 1),xl_rowcol_to_cell(k + 1, j + 1)))
                # sheet2.write(k + 1, j + 1, ((k + 1) * tempdf.at[i,'Max Bet1']) / (k + j + 2))
                sheet2.write_formula(k + 1, j + 1, '=({}*Sheet1!$B$2)/({}+{})'.format(xl_rowcol_to_cell(k + 1, 0),xl_rowcol_to_cell(k + 1, 0),xl_rowcol_to_cell(0, j + 1)))
                # sheet3.write(k + 1, j + 1, ((j + 1) * tempdf.at[i,'Max Bet2']) / (k + j + 2))
                sheet3.write_formula(k + 1, j + 1, '=({}*Sheet1!$C$2)/({}+{})'.format(xl_rowcol_to_cell(0, j + 1),xl_rowcol_to_cell(k + 1, 0),xl_rowcol_to_cell(0, j + 1)))
        wb.close()

def makedf_all3(df, names1, names2, bets1, bets2, bets3, casino,casinolist):
    #adds all of the fights to the final df, combining when it can

    for i in casinolist:
        if casino == i:
            bet1 = 'Bet1 {}'.format(i)
            bet2 = 'Bet2 {}'.format(i)
            bet3 = 'Bet3 {}'.format(i)

    #compares the df_all to the new df being added. If the fight names match, adds the bets, if not, adds the new fight to the end of the df.
    #this makes it so that this can be used for an infinite amount of casinos (assuming the relavent columns have been added)
    for i in range(len(names1)):
        for j in range(len(df.index)):
            if df.at[j,'Team 1'] == names1[i] and df.at[j,'Team 2'] == names2[i]:
                df.at[j, bet1] = bets1[i]
                df.at[j, bet2] = bets2[i]
                df.at[j, bet3] = bets3[i]
                break
            if j == len(df.index)-1:
                df = df.append({'Team 1': names1[i], bet1: bets1[i], 'Team 2': names2[i], bet2: bets2[i], bet3: bets3[i]},ignore_index=True)
    return df

def arbs3(df,casinolist):
    #finds the max bets
    df['Max Bet1'] = df.iloc[:, 1:len(casinolist) + 1].max(axis=1)
    df['Max Bet1 Casino'] = df.iloc[:, 1:len(casinolist) + 1].idxmax(axis='columns').str[-2:]

    df['Max Bet2'] = df.iloc[:, (5 + len(casinolist)):len(casinolist) + (5 + len(casinolist))].max(axis=1)
    df['Max Bet2 Casino'] = df.iloc[:, (5 + len(casinolist)):len(casinolist) + (5 + len(casinolist))].idxmax(axis='columns').str[-2:]
    #you will have to change the 5 to something else. Idk what it should be yet
    df['Max Bet3'] = df.iloc[:, (5 + len(casinolist)):len(casinolist) + (5 + len(casinolist))].max(axis=1)
    df['Max Bet3 Casino'] = df.iloc[:, (5 + len(casinolist)):len(casinolist) + (5 + len(casinolist))].idxmax(axis='columns').str[-2:]

    #converts max bets to non american odds
    df.loc[df['Max Bet1'] < 0, 'Max Bet1 Conv'] = (-100 / df['Max Bet1']) + 1
    df.loc[df['Max Bet1'] > 0, 'Max Bet1 Conv'] = (df['Max Bet1'] / 100) + 1
    df.loc[df['Max Bet2'] < 0, 'Max Bet2 Conv'] = (-100 / df['Max Bet2']) + 1
    df.loc[df['Max Bet2'] > 0, 'Max Bet2 Conv'] = (df['Max Bet2'] / 100) + 1
    df.loc[df['Max Bet3'] < 0, 'Max Bet3 Conv'] = (-100 / df['Max Bet3']) + 1
    df.loc[df['Max Bet3'] > 0, 'Max Bet3 Conv'] = (df['Max Bet3'] / 100) + 1

    #calculates arbs and fill NaN values
    df['Arb value'] = (1 / df['Max Bet1 Conv']) + (1 / df['Max Bet2 Conv']) + (1 / df['Max Bet3 Conv'])
    df.loc[df['Arb value'] <= 1, 'Arb'] = True
    df = df.fillna(value={'Arb': False})
    df = df.fillna(0)

    return df

def opss3(df):
    tempdf = pd.DataFrame()
    tempdf = tempdf.append(df.loc[df['Arb'] == True], ignore_index=True)

    for l in range(len(df.loc[df['Arb'] == True].index)):

        wb = xl.Workbook(tempdf.at[i, 'Team 1'] + ' vs ' + tempdf.at[i, 'Team 2'] + '.xlsx')
        sheet1 = wb.add_worksheet()
        sheet2 = wb.add_worksheet()
        sheet3 = wb.add_worksheet()
        sheet4 = wb.add_worksheet()

        # adding the formats used throughout the wb
        bold = wb.add_format({'bold': True})
        red_format = wb.add_format({'font_color': '#9C0006', 'bg_color': '#FFC7CE'})
        green_format = wb.add_format({'font_color': '#006100', 'bg_color': '#C6EFCE'})
        yellow_format = wb.add_format({'font_color': '#9C5700', 'bg_color': '#FFEB9C'})

        sheet1.write('B1', tempdf.at[l,'Team 1'], bold)
        sheet1.write('B2', tempdf.at[l,'Max Bet1 Conv'])
        sheet1.write('B3', tempdf.at[l,'Max Bet1 Casino'])
        sheet1.write('C1', tempdf.at[l,'Team 2'], bold)
        sheet1.write('C2', tempdf.at[l,'Max Bet2 Conv'])
        sheet1.write('C3', tempdf.at[l,'Max Bet2 Casino'])
        sheet1.write('D1', 'Tie', bold)
        sheet1.write('D2', tempdf.at[l,'Max Bet3 Conv'])
        sheet1.write('D3', tempdf.at[l,'Max Bet3 Casino'])

        sheet1.write('E1', 'Arb', bold)
        sheet1.write_formula('E2', '=(1/B2) + (1/C2) + (1/D2)')
        # applying the conditional formats
        sheet1.conditional_format('E2', {'type': 'cell', 'criteria': 'greater than', 'value': 1, 'format': red_format})
        sheet1.conditional_format('E2', {'type': 'cell', 'criteria': 'between', 'minimum': 0.95, 'maximum': 1,
                                         'format': green_format})
        sheet1.conditional_format('E2',
                                  {'type': 'cell', 'criteria': 'less than', 'value': 0.95, 'format': yellow_format})
        sheet2.conditional_format('C2:L101', {'type': 'cell', 'criteria': '>=', 'value': 1, 'format': green_format})
        sheet3.conditional_format('C2:L101', {'type': 'cell', 'criteria': '>=', 'value': 1, 'format': green_format})
        sheet4.conditional_format('C2:L101', {'type': 'cell', 'criteria': '>=', 'value': 1, 'format': green_format})
        sheet1.conditional_format('D6:M105', {'type': 'cell', 'criteria': '>=', 'value': 1, 'format': green_format})

        sheet1.write('C5', 'a,b,c', bold)
        sheet2.write('A1', 'a', bold)
        sheet2.write('B1', 'b', bold)
        sheet3.write('A1', 'a', bold)
        sheet3.write('B1', 'b', bold)
        sheet4.write('A1', 'a', bold)
        sheet4.write('B1', 'b', bold)
        for i in range(10):  # row a
            # add a and b values for each sheet
            sheet1.write(4, i + 3, i + 1, bold)
            sheet2.write(0, i + 2, i + 1, bold)
            sheet3.write(0, i + 2, i + 1, bold)
            sheet4.write(0, i + 2, i + 1, bold)
            for j in range(10):  # row b
                sheet1.write((j + 5) + (10 * i), 2, j + 1, bold)
                sheet1.write((j + 5) + (10 * i), 1, i + 1, bold)
                sheet2.write((j + 1) + (10 * i), 1, j + 1, bold)
                sheet2.write((j + 1) + (10 * i), 0, i + 1, bold)
                sheet3.write((j + 1) + (10 * i), 1, j + 1, bold)
                sheet3.write((j + 1) + (10 * i), 0, i + 1, bold)
                sheet4.write((j + 1) + (10 * i), 1, j + 1, bold)
                sheet4.write((j + 1) + (10 * i), 0, i + 1, bold)

                for k in range(10):
                    sheet1.write_formula((j + 5) + (10 * i), k + 3,
                                         '=IF(AND(Sheet2!{}>=1, Sheet3!{}>=1, Sheet4!{}>=1), 1, 0)'.format(
                                             xl_rowcol_to_cell((j + 1) + (i * 10), k + 2),
                                             xl_rowcol_to_cell((j + 1) + (i * 10), k + 2),
                                             xl_rowcol_to_cell((j + 1) + (i * 10), k + 2)))
                    sheet2.write_formula((j + 1) + (10 * i), k + 2,
                                         '=({}*Sheet1!$B$2)/({}+{}+{})'.format(xl_rowcol_to_cell((j + 1) + (i * 10), 0),
                                                                               xl_rowcol_to_cell((j + 1) + (i * 10), 0),
                                                                               xl_rowcol_to_cell((j + 1) + (i * 10), 1),
                                                                               xl_rowcol_to_cell(0, k + 2)))
                    sheet3.write_formula((j + 1) + (10 * i), k + 2,
                                         '=({}*Sheet1!$C$2)/({}+{}+{})'.format(xl_rowcol_to_cell((j + 1) + (i * 10), 1),
                                                                               xl_rowcol_to_cell((j + 1) + (i * 10), 0),
                                                                               xl_rowcol_to_cell((j + 1) + (i * 10), 1),
                                                                               xl_rowcol_to_cell(0, k + 2)))
                    sheet4.write_formula((j + 1) + (10 * i), k + 2,
                                         '=({}*Sheet1!$D$2)/({}+{}+{})'.format(xl_rowcol_to_cell(0, k + 2),
                                                                               xl_rowcol_to_cell((j + 1) + (i * 10), 0),
                                                                               xl_rowcol_to_cell((j + 1) + (i * 10), 1),
                                                                               xl_rowcol_to_cell(0, k + 2)))

        wb.close()
