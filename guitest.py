import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pandas import *
from numpy import nan


df1 = DataFrame({
    'Team 1': ['Bob', 'John', 'Billy', 'Nathan', 'Sam'],
    'Bet1 fd': [125, 195, -115, -175, 270],
    'Bet1 dk': [130, 200, -130, -180, 285],
    'Bet1 bm': [135, 185, -110, -165, 280],
    'Max Bet1': nan,
    'Max Bet1 Casino': nan,
    'Max Bet1 Conv': nan,
    'Team 2': ['Chris', 'Romeo', 'Blake', 'Philip', 'Jake'],
    'Bet2 fd': [-110, -180, 130, 180, -220],
    'Bet2 dk': [-120, -170, 110, 175, -225],
    'Bet2 bm': [-115, -165, 115, 170, -230],
    'Max Bet2': nan,
    'Max Bet2 Casino': nan,
    'Max Bet2 Conv': nan,
    'Arb value': nan,
    'Arb': nan
})

df2 = DataFrame({
    'Team 1': ['Bob2', 'John2', 'Billy2', 'Nathan2', 'Sam2'],
    'Bet1 fd': [130, 195, -115, -175, 270],
    'Bet1 dk': [130, 200, -130, -180, 285],
    'Bet1 bm': [135, 185, -110, -165, 280],
    'Max Bet1': nan,
    'Max Bet1 Casino': nan,
    'Max Bet1 Conv': nan,
    'Team 2': ['Chris2', 'Romeo2', 'Blake2', 'Philip2', 'Jake2'],
    'Bet2 fd': [-110, -180, 130, 180, -220],
    'Bet2 dk': [-110, -170, 110, 175, -225],
    'Bet2 bm': [-115, -165, 115, 170, -230],
    'Max Bet2': nan,
    'Max Bet2 Casino': nan,
    'Max Bet2 Conv': nan,
    'Arb value': nan,
    'Arb': nan
})

dfs = [df1, df2]
casinos = ['dk','fd','bm']

for df in dfs:
    df['Max Bet1'] = df[{'Bet1 dk', 'Bet1 fd', 'Bet1 bm'}].max(axis=1)
    df['Max Bet1 Casino'] = df[{'Bet1 dk', 'Bet1 fd', 'Bet1 bm'}].idxmax(axis='columns').str[-2:]

    df['Max Bet2'] = df[{'Bet2 dk', 'Bet2 fd', 'Bet2 bm'}].max(axis=1)
    df['Max Bet2 Casino'] = df[{'Bet2 dk', 'Bet2 fd', 'Bet2 bm'}].idxmax(axis='columns').str[-2:]

    df.loc[df['Max Bet1'] < 0, 'Max Bet1 Conv'] = (-100 / df['Max Bet1']) + 1
    df.loc[df['Max Bet1'] > 0, 'Max Bet1 Conv'] = (df['Max Bet1'] / 100) + 1
    df.loc[df['Max Bet2'] < 0, 'Max Bet2 Conv'] = (-100 / df['Max Bet2']) + 1
    df.loc[df['Max Bet2'] > 0, 'Max Bet2 Conv'] = (df['Max Bet2'] / 100) + 1

    df['Arb value'] = (1 / df['Max Bet1 Conv']) + (1 / df['Max Bet2 Conv'])
    df.loc[df['Arb value'] <= 1, 'Arb'] = True
    values = {'Bet1 dk':0,'Bet1 fd':0,'Bet1 bm':0,'Bet2 dk':0,'Bet2 fd':0,'Bet2 bm':0,'Arb':False}
    df = df.fillna(value=values)


class DisplayDataFrame(QTableView): #have it display the dataframe and only the important columns. The user can then select a match to expand
    def __init__(self, dataFrame:DataFrame):
        super().__init__()
        self.data = dataFrame
        # for i in range(len(self.data.index)):
        #     pass
        self.model = PandasModel(self.data)
        self.setModel(self.model)
        self.setFont(QFont('IDK',15))
        self.resizeColumnsToContents()
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
    

class PandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role):
        if index.isValid():
            value = self._data.iloc[index.row(), index.column()]
            if role == Qt.DisplayRole:
                if isinstance(value, float):
                    return str(round(value, 4))
                return str(value)
            elif role == Qt.BackgroundRole:
                if self._data.columns[index.column()] == 'Arb' and value == True:
                    return QColor('green')
                elif self._data.columns[index.column()] == 'Arb value':
                    if value >= 1:
                        return QColor('red')
                    elif 1 > value >= 0.95:
                        return QColor('green')
                    else:
                        return QColor('yellow')
            elif role == Qt.TextAlignmentRole:
                if isinstance(value, float) or isinstance(value, int):
                    return Qt.AlignRight
        return None

    def headerData(self, index, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[index]
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            return index+1
        return None


class Match(QWidget):
    def __init__(self, casinos):
        super().__init__()
        self.casinos = casinos
        self.setMaximumWidth(400)
        self.setMinimumWidth(400)
        self.matchlayout = QGridLayout()
        self.setLayout(self.matchlayout)
        self.team1L = QLabel('')
        self.team1L.setFont(QFont('IDK',20))
        self.team2L = QLabel('')
        self.team2L.setFont(QFont('IDK',20))
        self.vsL = QLabel('vs')
        self.vsL.setFont(QFont('IDK',20))
        self.arbL = QLabel('Arb Value')
        self.arbL.setFont(QFont('IDK',20))
        self.arbValL = QLabel('')
        self.arbValL.setFont(QFont('IDK',20))
        self.totalBetL = QLabel('Total Bet')
        self.totalBetL.setFont(QFont('IDK',20))
        self.totalBetText = QLineEdit()
        self.totalBetText.setFont(QFont('IDK',20))
        self.totalBetText.setPlaceholderText('Total Bet Amount')
        self.totalBetText.setAlignment(Qt.AlignCenter)
        validator = QDoubleValidator(bottom=0, decimals=2)
        self.totalBetText.setValidator(validator)
        self.totalBetText.setMaxLength(12)
        self.calculateTeamBets = QPushButton('Calculate Bets')
        self.calculateTeamBets.setFont(QFont('IDK',20))
        self.totalBet1L = QLabel('Bet1')
        self.totalBet1L.setFont(QFont('IDK',20))
        self.totalBet1ValL = QLabel('$0')
        self.totalBet1ValL.setFont(QFont('IDK',20))
        self.totalBet2L = QLabel('Bet2')
        self.totalBet2L.setFont(QFont('IDK',20))
        self.totalBet2ValL = QLabel('$0')
        self.totalBet2ValL.setFont(QFont('IDK',20))
        self.estProfitL = QLabel('Estimated Profit')
        self.estProfitL.setFont(QFont('IDK',20))
        self.estProfitValL = QLabel('$0')
        self.estProfitValL.setFont(QFont('IDK',20))

        self.matchlayout.addWidget(self.team1L, 0, 0, alignment=Qt.AlignCenter)
        self.matchlayout.addWidget(self.team2L, 0, 2, alignment=Qt.AlignCenter)
        self.matchlayout.addWidget(self.vsL, 0, 1, alignment=Qt.AlignCenter)
        for i in range(len(self.casinos)):
            self.casinoL = QLabel(self.casinos[i])
            self.casinoL.setFont(QFont('IDK',20))
            self.matchlayout.addWidget(self.casinoL, i+1, 1, alignment=Qt.AlignCenter)

        self.matchlayout.addWidget(self.arbL, 2 + len(self.casinos), 1, alignment=Qt.AlignCenter)
        self.matchlayout.addWidget(self.arbValL, 3 + len(self.casinos), 1, alignment=Qt.AlignCenter)
        self.matchlayout.addWidget(self.totalBetL, 4 + len(self.casinos), 1, alignment=Qt.AlignCenter)
        self.matchlayout.addWidget(self.totalBetText, 5 + len(self.casinos), 1, alignment=Qt.AlignCenter)
        self.matchlayout.addWidget(self.totalBet1L, 5 + len(self.casinos), 0, alignment=Qt.AlignCenter)
        self.matchlayout.addWidget(self.totalBet2L, 5 + len(self.casinos), 2, alignment=Qt.AlignCenter)
        self.matchlayout.addWidget(self.calculateTeamBets, 6 + len(self.casinos), 1, alignment=Qt.AlignCenter)
        self.matchlayout.addWidget(self.totalBet1ValL, 6 + len(self.casinos), 0, alignment=Qt.AlignCenter)
        self.matchlayout.addWidget(self.totalBet2ValL, 6 + len(self.casinos), 2, alignment=Qt.AlignCenter)
        self.matchlayout.addWidget(self.estProfitL, 7 + len(self.casinos), 1, alignment=Qt.AlignCenter)
        self.matchlayout.addWidget(self.estProfitValL, 8 + len(self.casinos), 1, alignment=Qt.AlignCenter)


class DataViewWindow(QMainWindow):
    def __init__(self, dataFrames, casinos):
        super().__init__()
        self.main = QWidget()
        self.data = dataFrames
        self.setWindowTitle('Data')
        self.setMinimumWidth(1575)
        # self.resize(1575, 500)

        self.currentTab = None
        self.currentRow = None
        self.casinos = casinos
        self.tabs = QTabWidget()
        self.setCentralWidget(self.main)
        self.hori = QHBoxLayout()

        for i in range(len(dataFrames)):
            newTab = QWidget()
            layout = QVBoxLayout()
            table = DisplayDataFrame(dataFrames[i])
            table.setObjectName('dataframe{}'.format(i))
            table.doubleClicked.connect(self.updateMatch)
            layout.addWidget(table)
            newTab.setLayout(layout)
            self.tabs.addTab(newTab, 'Tab {}'.format(i))
            table.show()
        
        self.hori.addWidget(self.tabs)
        self.main.setLayout(self.hori)

        self.match = Match(self.casinos)
        self.match.totalBetText.returnPressed.connect(self.calculateBets)
        self.match.calculateTeamBets.clicked.connect(self.calculateBets)
        self.hori.addWidget(self.match)
        self.match.setVisible(False)

    def updateMatch(self, index):
        
        row = index.row()
        frame = self.tabs.currentIndex()

        if self.currentRow == row and self.currentTab == frame:
            return None

        self.match.setVisible(True)
        name1 = self.data[frame].at[row, 'Team 1']
        name2 = self.data[frame].at[row, 'Team 2']
        maxOdd1 = self.data[frame].at[row, 'Max Bet1']
        maxOdd2 = self.data[frame].at[row, 'Max Bet2']
        arbVal = round(self.data[frame].at[row, 'Arb value'], 4)

        self.match.team1L.setText(name1)
        self.match.team2L.setText(name2)
        self.match.arbValL.setText(str(arbVal))

        for i in range(len(self.casinos)):
            newOdd1 = self.data[frame].at[row, 'Bet1 {}'.format(self.casinos[i])]
            newOdd2 = self.data[frame].at[row, 'Bet2 {}'.format(self.casinos[i])]
            
            
            if self.match.matchlayout.itemAtPosition(i+1, 0) == None:
                self.odd1L = QLabel(str(newOdd1))
                self.odd1L.setFont(QFont('IDK',20))
                self.odd2L = QLabel(str(newOdd2))
                self.odd2L.setFont(QFont('IDK',20))

                self.match.matchlayout.addWidget(self.odd1L, i+1, 0, alignment=Qt.AlignCenter)
                self.match.matchlayout.addWidget(self.odd2L, i+1, 2, alignment=Qt.AlignCenter)
            else:
                odd1 = self.match.matchlayout.itemAtPosition(i+1, 0)
                widgetodd1 = odd1.widget()
                widgetodd1.setStyleSheet('')
                widgetodd1.setText(str(newOdd1))
                odd2 = self.match.matchlayout.itemAtPosition(i+1, 2)
                widgetodd2 = odd2.widget()
                widgetodd2.setStyleSheet('')
                widgetodd2.setText(str(newOdd2))

            if newOdd1 == maxOdd1:
                maxodd1 = self.match.matchlayout.itemAtPosition(i+1, 0)
                widgetmaxodd1 = maxodd1.widget()
                widgetmaxodd1.setStyleSheet('background: #FFFFFF; border: 2px solid black')
            if newOdd2 == maxOdd2:
                maxodd2 = self.match.matchlayout.itemAtPosition(i+1, 2)
                widgetmaxodd2 = maxodd2.widget()
                widgetmaxodd2.setStyleSheet('background: #FFFFFF; border: 2px solid black')

            self.currentTab = frame
            self.currentRow = row


    def calculateBets(self):
        bet = float(self.match.totalBetText.text())
        maxA = self.data[self.currentTab].at[self.currentRow, 'Max Bet1 Conv']
        maxB = self.data[self.currentTab].at[self.currentRow, 'Max Bet2 Conv']
        betA = round(bet/(1 + (maxA/maxB)), 2)
        betB = round(bet/(1 + (maxB/maxA)), 2)
        profit = round(bet*( ((maxA*maxB) - (maxA + maxB))/ (maxA + maxB) ), 2)
        self.match.totalBet1ValL.setText('${}'.format(str(betA)))
        self.match.totalBet2ValL.setText('${}'.format(str(betB)))
        self.match.estProfitValL.setText('${}'.format(str(profit)))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Arbitrage Betting')
        self.setMaximumSize(500, 400)
        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        self.title = QLabel('Arbitrage Betting')
        self.title.setFont(QFont('IDK',40))
        self.mlb = QCheckBox('MLB')
        self.mlb.setFont(QFont('IDK',20))
        self.nhl = QCheckBox('NHL')
        self.nhl.setFont(QFont('IDK',20))
        self.ufc = QCheckBox('UFC')
        self.ufc.setFont(QFont('IDK',20))
        self.nba = QCheckBox('NBA')
        self.nba.setFont(QFont('IDK',20))
        self.mls = QCheckBox('MLS')
        self.mls.setFont(QFont('IDK',20))
        self.checkAllButton = QPushButton('Select All', clicked=self.checkAll)
        self.checkAllButton.setFont(QFont('IDK',15))
        self.uncheckAllButton = QPushButton('Deselect All', clicked=self.uncheckAll)
        self.uncheckAllButton.setFont(QFont('IDK',15))
        self.findArbButton = QPushButton('Find Arbs', clicked=self.findArbs)
        self.findArbButton.setFont(QFont('IDK',15))

        # self.checkAllButton.clicked.connect(self.checkAll)
        # self.uncheckAllButton.clicked.connect(self.uncheckAll)
        # self.findArbButton.clicked.connect(self.findArbs)

        g = QGridLayout()
        g.addWidget(self.title, 0, 0, 1, 2, alignment=Qt.AlignCenter | Qt.AlignTop)
        g.addWidget(self.mlb, 1, 0, alignment=Qt.AlignCenter)
        g.addWidget(self.nhl, 1, 1, alignment=Qt.AlignCenter)
        g.addWidget(self.ufc, 2, 0, alignment=Qt.AlignCenter)
        g.addWidget(self.nba, 2, 1, alignment=Qt.AlignCenter)
        g.addWidget(self.mls, 3, 0, alignment=Qt.AlignCenter)
        g.addWidget(self.checkAllButton, 4, 0)
        g.addWidget(self.uncheckAllButton, 4, 1)
        g.addWidget(self.findArbButton, 5, 0, 1, 2)

        self.widget.setLayout(g)
        self.sportOptions = [self.mlb, self.nhl, self.ufc, self.nba, self.mls]

    def checkAll(self):
        for sport in self.sportOptions:
            sport.setChecked(True)

    def uncheckAll(self):
        for sport in self.sportOptions:
            sport.setChecked(False)

    def findArbs(self):
        sports = []
        for sport in self.sportOptions:
            if sport.isChecked() == True:
                sports.append(sport.text().lower())
        print(sports)
        if sports == []:
            msg = QMessageBox()
            msg.setText('At least 1 sport must be selected to begine finding viable arbs')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:# this will be the code in the main file to find the arbs
            self.data = DataViewWindow(dfs, casinos)
            self.data.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # model = PandasModel(df1)
    # view = QTableView()
    # view.setModel(model)
    # view.setFont(QFont('IDK',15))
    # view.resizeColumnsToContents()
    # view.show()
    app.exec_()
