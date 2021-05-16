from numpy import nan
import xlsxwriter as xl
import pandas as pd


def alphabetize(names1:list, names2:list, bets1:list, bets2:list) -> list:
    #rearranges the fighters so that the first and second names are in alphabetical order
    for i in range(len(names1)):
        if names1[i] > names2[i]:
            names1[i], names2[i] = names2[i], names1[i] #swaps the names
            bets1[i], bets2[i] = bets2[i], bets1[i] #swaps the bets
    return names1, names2, bets1, bets2

def singleconvert(odd:str) -> int:
    #converts the data from string to the int odds for future calcs
    #If the odd cannot convert the input into a number, it makes the odd -9999
    try:
        convint = int(odd.replace("+", ""))
    except:
        convint = -9999
    return convint

def makedf_all(df:pd.DataFrame, names1:list, names2:list, bets1:list, bets2:list, casino:str) -> pd.DataFrame:
    #adds all of the fights to the final df, combining when it can

    bet1 = 'Bet1 {}'.format(casino)
    bet2 = 'Bet2 {}'.format(casino)

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

def arbs(df:pd.DataFrame, casinolist:list) -> pd.DataFrame:
    #finds the max bets
    df['Max Bet1'] = df.iloc[:,1:len(casinolist)+1].max(axis=1)
    df['Max Bet1 Casino'] = df.iloc[:,1:len(casinolist)+1].idxmax(axis='columns').str[-2:] #if there is an error here, remove '.str[-2:]' and uncomment the line below
    # df['Max Bet1 Casino'] = df['Max Bet1 Casino'].str[-2:]

    df['Max Bet2'] = df.iloc[:,(5+len(casinolist)):len(casinolist)+(5+len(casinolist))].max(axis=1)
    df['Max Bet2 Casino'] = df.iloc[:,(5+len(casinolist)):len(casinolist)+(5+len(casinolist))].idxmax(axis='columns').str[-2:] #if there is an error here, remove '.str[-2:]' and uncomment the line below
    # df['Max Bet2 Casino'] = df['Max Bet2 Casino'][-2:]

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

def opss(df:pd.DataFrame):
    #output spreadsheet for all viable arbs
    tempdf = pd.DataFrame()
    tempdf = tempdf.append(df.loc[df['Arb'] is True], ignore_index=True)
    # for i in range(len(df['Max Bet1 Conv'].loc[df['Arb'] is True].index)): #might be able to get rid of the 'Max Bet1' part
    for i in range(len(tempdf.index)):
        wb = xl.Workbook('arbs\{} vs {}.xlsx'.format(tempdf.at[i, 'Team 1'], tempdf.at[i, 'Team 2']))
        sheet1 = wb.add_worksheet()

        # adding the formats used throughout the wb
        red_format = wb.add_format({'font_color': '#9C0006', 'bg_color': '#FFC7CE'})
        green_format = wb.add_format({'font_color': '#006100', 'bg_color': '#C6EFCE'})
        yellow_format = wb.add_format({'font_color': '#9C5700', 'bg_color': '#FFEB9C'})
        top_border_format = wb.add_format({'border': 1, 'bottom': 0, 'bold': True})
        bottom_border_format = wb.add_format({'border': 1, 'top': 0})
        bottom_border_format_percent = wb.add_format({'border': 1, 'top': 0, 'num_format': '0.00%'})
        mergeformat = wb.add_format({'border': 1, 'bottom': 0, 'align': 'center', 'valign': 'vcenter', 'bold': True})
        mergeformat2 = wb.add_format({'border': 1, 'top': 0, 'align': 'center', 'valign': 'vcenter'})

        sheet1.write('B1', tempdf.at[i, 'Team 1'], top_border_format)
        sheet1.write('B2', tempdf.at[i, 'Max Bet1 Conv'], bottom_border_format)
        sheet1.write('B3', tempdf.at[i, 'Max Bet1 Casino'], bottom_border_format)
        sheet1.write('C1', tempdf.at[i, 'Team 2'], top_border_format)
        sheet1.write('C2', tempdf.at[i, 'Max Bet2 Conv'], bottom_border_format)
        sheet1.write('C3', tempdf.at[i, 'Max Bet2 Casino'], bottom_border_format)

        sheet1.write('D1', 'Arb', top_border_format)
        sheet1.write_formula('D2', '=(1/B2) + (1/C2)', bottom_border_format)
        # applying the conditional formats
        sheet1.conditional_format('D2', {'type': 'cell', 'criteria': 'greater than', 'value': 1, 'format': red_format})
        sheet1.conditional_format('D2', {'type': 'cell', 'criteria': 'between', 'minimum': 0.95, 'maximum': 1, 'format': green_format})
        sheet1.conditional_format('D2', {'type': 'cell', 'criteria': 'less than', 'value': 0.95, 'format': yellow_format})

        sheet1.merge_range('E1:F1', 'Total Bet', mergeformat)
        sheet1.merge_range('E2:F2', 0, mergeformat2)

        sheet1.write('B4', 'Bet on {}'.format(tempdf.at[i, 'Team 1']), top_border_format)
        sheet1.write_formula('B5', '=E2/((B2/C2)+1)', bottom_border_format)
        sheet1.write('B6', 'Profit if {} wins'.format(tempdf.at[i, 'Team 1']), top_border_format)
        sheet1.write_formula('B7', '=B5*(B2-1)-C5', bottom_border_format)
        sheet1.write('C4', 'Bet on {}'.format(tempdf.at[i, 'Team 2']), top_border_format)
        sheet1.write_formula('C5', '=E2/((C2/B2)+1)', bottom_border_format)
        sheet1.write('C6', 'Profit if {} wins'.format(tempdf.at[i, 'Team 2']), top_border_format)
        sheet1.write_formula('C7', '=C5*(C2-1)-B5', bottom_border_format)

        sheet1.set_column('B:B', round(len('Profit if {} wins'.format(tempdf.at[i, 'Team 1'])) * 0.9), 0)
        sheet1.set_column('C:C', round(len('Profit if {} wins'.format(tempdf.at[i, 'Team 2'])) * 0.9), 0)

        sheet1.write('D3', 'Approximate Profit %', top_border_format)
        sheet1.write_formula('D4', '=((B2*C2)-(B2+C2))/(B2+C2)', bottom_border_format_percent)
        sheet1.set_column('D:D', 19)
        wb.close()

def makedf_all3outcome(df:pd.DataFrame, names1:list, names2:list, bets1:list, bets2:list, bets3:list, casino:str) -> pd.DataFrame:
    #adds all of the fights to the final df, combining when it can

    bet1 = 'Bet1 {}'.format(casino)
    bet2 = 'Bet2 {}'.format(casino)
    bet3 = 'Bet3 {}'.format(casino)

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

def arbs3outcome(df:pd.DataFrame,casinolist:list) -> pd.DataFrame:
    #finds the max bets
    df['Max Bet1'] = df.iloc[:, 1:len(casinolist) + 1].max(axis=1)
    df['Max Bet1 Casino'] = df.iloc[:, 1:len(casinolist) + 1].idxmax(axis='columns').str[-2:] #if there is an error here, remove '.str[-2:]' and uncomment the line below
    # df['Max Bet1 Casino'] = df['Max Bet1 Casino'].str[-2:]

    df['Max Bet2'] = df.iloc[:, (5 + len(casinolist)):len(casinolist) + (5 + len(casinolist))].max(axis=1)
    df['Max Bet2 Casino'] = df.iloc[:, (5 + len(casinolist)):len(casinolist) + (5 + len(casinolist))].idxmax(axis='columns').str[-2:] #if there is an error here, remove '.str[-2:]' and uncomment the line below
    # df['Max Bet2 Casino'] = df['Max Bet2 Casino'].str[-2:]
    #you will have to change the 5 to something else. Idk what it should be yet
    df['Max Bet3'] = df.iloc[:, (5 + len(casinolist)):len(casinolist) + (5 + len(casinolist))].max(axis=1)
    df['Max Bet3 Casino'] = df.iloc[:, (5 + len(casinolist)):len(casinolist) + (5 + len(casinolist))].idxmax(axis='columns').str[-2:] #if there is an error here, remove '.str[-2:]' and uncomment the line below
    # df['Max Bet3 Casino'] = df['Max Bet3 Casino'].str[-2:]

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

def opss3outcome(df:pd.DataFrame):
    tempdf = pd.DataFrame()
    tempdf = tempdf.append(df.loc[df['Arb'] is True], ignore_index=True)

    # for l in range(len(df.loc[df['Arb'] is True].index)):
    for l in range(len(tempdf.index)):
        wb = xl.Workbook('arbs\{} vs {}.xlsx'.format(tempdf.at[l, 'Team 1'], tempdf.at[l, 'Team 2']))
        sheet1 = wb.add_worksheet()

        # adding the formats used throughout the wb
        red_format = wb.add_format({'font_color': '#9C0006', 'bg_color': '#FFC7CE'})
        green_format = wb.add_format({'font_color': '#006100', 'bg_color': '#C6EFCE'})
        yellow_format = wb.add_format({'font_color': '#9C5700', 'bg_color': '#FFEB9C'})
        top_border_format = wb.add_format({'border': 1, 'bottom': 0, 'bold': True})
        bottom_border_format = wb.add_format({'border': 1, 'top': 0})
        bottom_border_format_percent = wb.add_format({'border': 1, 'top': 0, 'num_format': '0.00%'})
        mergeformat = wb.add_format({'border': 1, 'bottom': 0, 'align': 'center', 'valign': 'vcenter', 'bold': True})
        mergeformat2 = wb.add_format({'border': 1, 'top': 0, 'align': 'center', 'valign': 'vcenter'})

        sheet1.write('B1', tempdf.at[l, 'Team 1'], top_border_format)
        sheet1.write('B2', tempdf.at[l, 'Max Bet1 Conv'], bottom_border_format)
        sheet1.write('B3', tempdf.at[l, 'Max Bet1 Casino'], bottom_border_format)
        sheet1.write('C1', tempdf.at[l, 'Team 2'], top_border_format)
        sheet1.write('C2', tempdf.at[l, 'Max Bet2 Conv'], bottom_border_format)
        sheet1.write('C3', tempdf.at[l, 'Max Bet2 Casino'], bottom_border_format)
        sheet1.write('D1', 'Draw', top_border_format)
        sheet1.write('D2', tempdf.at[l, 'Max Bet3 Conv'], bottom_border_format)
        sheet1.write('D3', tempdf.at[l, 'Max Bet3 Casino'], bottom_border_format)

        sheet1.write('E1', 'Arb', top_border_format)
        sheet1.write_formula('E2', '=(1/B2) + (1/C2) + (1/D2)', bottom_border_format)
        # applying the conditional formats
        sheet1.conditional_format('E2', {'type': 'cell', 'criteria': 'greater than', 'value': 1, 'format': red_format})
        sheet1.conditional_format('E2', {'type': 'cell', 'criteria': 'between', 'minimum': 0.95, 'maximum': 1, 'format': green_format})
        sheet1.conditional_format('E2', {'type': 'cell', 'criteria': 'less than', 'value': 0.95, 'format': yellow_format})

        sheet1.merge_range('F1:G1', 'Total Bet', mergeformat)
        sheet1.merge_range('F2:G3', 0, mergeformat2)

        sheet1.write('B4', 'Bet on {}'.format(tempdf.at[l, 'Team 1']), top_border_format)
        sheet1.write_formula('B5', '=F2/((B2/C2)+(B2/D2)+1)', bottom_border_format)
        sheet1.write('B6', 'Profit if {} wins'.format(tempdf.at[l, 'Team 1']), top_border_format)
        sheet1.write_formula('B7', '=B5*(B2-1)-C5-D5', bottom_border_format)
        sheet1.write('C4', 'Bet on {}'.format(tempdf.at[l, 'Team 2']), top_border_format)
        sheet1.write_formula('C5', '=F2/((C2/B2)+(C2/D2)+1)', bottom_border_format)
        sheet1.write('C6', 'Profit if {} wins'.format(tempdf.at[l, 'Team 2']), top_border_format)
        sheet1.write_formula('C7', '=C5*(C2-1)-B5-D5', bottom_border_format)
        sheet1.write('D4', 'Bet on Draw', top_border_format)
        sheet1.write_formula('D5', '=F2/((D2/B2)+(D2/C2)+1)', bottom_border_format)
        sheet1.write('D6', 'Profit if they draw', top_border_format)
        sheet1.write_formula('D7', '=D5*(D2-1)-B5-C5', bottom_border_format)

        sheet1.set_column('B:B', round(len('Profit if {} wins'.format(tempdf.at[l, 'Team 1'])) * 0.9), 0)
        sheet1.set_column('C:C', round(len('Profit if {} wins'.format(tempdf.at[l, 'Team 2'])) * 0.9), 0)
        sheet1.set_column('D:D', round(len('Profit if they tie') * 0.9), 0)

        sheet1.write('E3', 'Approximate Profit %', top_border_format)
        sheet1.write_formula('E4', '=((B2*C2*D2)-(B2*C2)-(B2*D2)-(C2*D2))/((B2*C2)+(B2*D2)+(C2*D2))', bottom_border_format_percent)
        sheet1.set_column('E:E', 19)

        wb.close()
