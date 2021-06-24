import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pandas import *
from numpy import nan


df1 = DataFrame({
    'Name1': ['Bob', 'John', 'Billy', 'Nathan', 'Sam'],
    'Bet1 fd': [125, 195, -115, -175, 270],
    'Bet1 dk': [130, 200, -130, -180, 285],
    'Bet1 bm': [135, 185, -110, -165, 280],
    'Max Bet1': nan,
    'Max Bet1 Casino': nan,
    'Max Bet1 Conv': nan,
    'Name2': ['Chris', 'Romeo', 'Blake', 'Philip', 'Jake'],
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
    'Name1': ['Bob2', 'John2', 'Billy2', 'Nathan2', 'Sam2'],
    'Bet1 fd': [130, 195, -115, -175, 270],
    'Bet1 dk': [130, 200, -130, -180, 285],
    'Bet1 bm': [135, 185, -110, -165, 280],
    'Max Bet1': nan,
    'Max Bet1 Casino': nan,
    'Max Bet1 Conv': nan,
    'Name2': ['Chris2', 'Romeo2', 'Blake2', 'Philip2', 'Jake2'],
    'Bet2 fd': [-110, -180, 130, 180, -220],
    'Bet2 dk': [-120, -170, 110, 175, -225],
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



# df1['Max Bet1'] = df1[{'Bet1 dk', 'Bet1 fd', 'Bet1 bm'}].max(axis=1)
# df1['Max Bet1 Casino'] = df1[{'Bet1 dk', 'Bet1 fd', 'Bet1 bm'}].idxmax(axis='columns').str[-2:]

# df1['Max Bet2'] = df1[{'Bet2 dk', 'Bet2 fd', 'Bet2 bm'}].max(axis=1)
# df1['Max Bet2 Casino'] = df1[{'Bet2 dk', 'Bet2 fd', 'Bet2 bm'}].idxmax(axis='columns').str[-2:]

# df1.loc[df1['Max Bet1'] < 0, 'Max Bet1 Conv'] = (-100 / df1['Max Bet1']) + 1
# df1.loc[df1['Max Bet1'] > 0, 'Max Bet1 Conv'] = (df1['Max Bet1'] / 100) + 1
# df1.loc[df1['Max Bet2'] < 0, 'Max Bet2 Conv'] = (-100 / df1['Max Bet2']) + 1
# df1.loc[df1['Max Bet2'] > 0, 'Max Bet2 Conv'] = (df1['Max Bet2'] / 100) + 1

# df1['Arb value'] = (1 / df1['Max Bet1 Conv']) + (1 / df1['Max Bet2 Conv'])
# df1.loc[df1['Arb value'] <= 1, 'Arb'] = True
# values = {'Bet1 dk':0,'Bet1 fd':0,'Bet1 bm':0,'Bet2 dk':0,'Bet2 fd':0,'Bet2 bm':0,'Arb':False}
# df1 = df1.fillna(value=values)
# print(df1)



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
        self.doubleClicked.connect(self.testing)
    
    def testing(self, index):
        print(index.row())


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
                    return str(round(value, 3))
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

class DataViewWindow(QMainWindow):
    def __init__(self, dataFrames):
        super().__init__()

        self.setWindowTitle('Data')
        self.setBaseSize(800, 500)
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        for i in range(len(dataFrames)):
            newTab = QWidget()
            layout = QVBoxLayout()
            table = DisplayDataFrame(dataFrames[i])
            layout.addWidget(table)
            newTab.setLayout(layout)
            self.tabs.addTab(newTab, 'Tab {}'.format(i))
            table.show()



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
            self.data = DataViewWindow(dfs)
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
