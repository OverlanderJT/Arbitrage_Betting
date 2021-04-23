from tkinter import *
from tkscrolledframe import ScrolledFrame
from pandas import *
from numpy import nan


def selectall():
    var1.set(1)
    var2.set(1)
    var3.set(1)
    var4.set(1)
    var5.set(1)
    var6.set(1)


def deselectall():
    var1.set(0)
    var2.set(0)
    var3.set(0)
    var4.set(0)
    var5.set(0)
    var6.set(0)


def getarb():
    if var1.get() == 1:
        print('UFC')
    if var2.get() == 1:
        print('NBA')
    if var3.get() == 1:
        print('NHL')
    if var4.get() == 1:
        print('MLB')
    if var5.get() == 1:
        print('Soccer')
    if var6.get() == 1:
        print('NFL')


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


df1['Max Bet1'] = df1[{'Bet1 dk', 'Bet1 fd', 'Bet1 bm'}].max(axis=1)
df1['Max Bet1 Casino'] = df1[{'Bet1 dk', 'Bet1 fd', 'Bet1 bm'}].idxmax(axis='columns').str[-2:]

df1['Max Bet2'] = df1[{'Bet2 dk', 'Bet2 fd', 'Bet2 bm'}].max(axis=1)
df1['Max Bet2 Casino'] = df1[{'Bet2 dk', 'Bet2 fd', 'Bet2 bm'}].idxmax(axis='columns').str[-2:]

df1.loc[df1['Max Bet1'] < 0, 'Max Bet1 Conv'] = (-100 / df1['Max Bet1']) + 1
df1.loc[df1['Max Bet1'] > 0, 'Max Bet1 Conv'] = (df1['Max Bet1'] / 100) + 1
df1.loc[df1['Max Bet2'] < 0, 'Max Bet2 Conv'] = (-100 / df1['Max Bet2']) + 1
df1.loc[df1['Max Bet2'] > 0, 'Max Bet2 Conv'] = (df1['Max Bet2'] / 100) + 1

df1['Arb value'] = (1 / df1['Max Bet1 Conv']) + (1 / df1['Max Bet2 Conv'])
df1.loc[df1['Arb value'] <= 1, 'Arb'] = True
values = {'Bet1 dk':0,'Bet1 fd':0,'Bet1 bm':0,'Bet2 dk':0,'Bet2 fd':0,'Bet2 bm':0,'Arb':False}
df1 = df1.fillna(value=values)
print(df1)


#creating the main menu window and all necessary widghets
root = Tk()
root.title('Arbitrage Betting')
l1 = Label(root,text="Arbitrage Betting",font=("Arial",50)).pack()
f = Frame(root)
f.pack()
f2 = Frame(root)
f2.pack()

var1 = IntVar() #creating and setting the variables for the check boxes
var2 = IntVar()
var3 = IntVar()
var4 = IntVar()
var5 = IntVar()
var6 = IntVar()
#creating all of the widgets for main menu
check1 = Checkbutton(f,text='MMA',font=("Arial",20),variable=var1,width=10,relief='groove').grid(row=0,column=0,pady=10,padx=10)
check2 = Checkbutton(f,text='Basketball',font=("Arial",20),variable=var2,width=10,relief='groove').grid(row=0,column=1,pady=10,padx=10)
check3 = Checkbutton(f,text='Hockey',font=("Arial",20),variable=var3,width=10,relief='groove').grid(row=1,column=0,pady=10,padx=10)
check4 = Checkbutton(f,text='Baseball',font=("Arial",20),variable=var4,width=10,relief='groove').grid(row=1,column=1,pady=10,padx=10)
check5 = Checkbutton(f,text='Soccer',font=("Arial",20),variable=var5,width=10,relief='groove').grid(row=2,column=0,pady=10,padx=10)
check6 = Checkbutton(f,text='Football',font=("Arial",20),variable=var6,width=10,relief='groove').grid(row=2,column=1,pady=10,padx=10)
checkall = Button(f2,text='Select All',font=('Arial',13),borderwidth=3,relief='raised',command=selectall).pack(side='left')
uncheckall = Button(f2,text='Deselect All',font=('Arial',13),borderwidth=3,relief='raised',command=deselectall).pack(side='right')
gen = Button(root,text="Find Arbs",font=("Arial",20),borderwidth=5,relief='raised',command=getarb).pack()

#Creating the second window to display the arbs (This would be done when the "Find Arbs" button from the main menu is pressed
root2 = Tk()
root2.title('Arbs')
root2.geometry('1400x900')

sf = ScrolledFrame(root2) #making the window scroll if needed
sf.pack(expand='yes',fill='both')
sf.bind_arrow_keys(root2)
sf.bind_scroll_wheel(root2)
innerf = sf.display_widget(Frame)

lf2 = LabelFrame(innerf,text='UFC',font=("Arial",20))
lf2.pack(fill='both',expand='yes',pady=10,padx=15)

for i in range(len(df1)):
    for j in range(6):
        if (i*4)+j == len(df1):
            break
        frame = LabelFrame(lf2,width=290,height=110)
        frame.grid(row=i,column=j,pady=5,padx=10)
        frame.pack_propagate(0)

        name1 = Label(frame, text='{}'.format(df1.at[(i*4)+j,'Name1']),font=("Arial",20))
        name1.place(relx=0.44, rely=0, anchor='ne')
        vs = Label(frame, text='vs', font=("Arial", 20))
        vs.place(relx=0.5,rely=0,anchor='n')
        name2 = Label(frame, text='{}'.format(df1.at[(i * 4) + j, 'Name2']), font=("Arial", 20))
        name2.place(relx=0.56, rely=0, anchor='nw')

        l2 = Label(frame,text='{}  {}'.format(df1.at[(i*4)+j,'Max Bet1'],df1.at[(i*4)+j,'Max Bet1 Casino']),font=("Arial",14))
        l2.place(relx=0.44, rely=0.325, anchor='ne')

        l3 = Label(frame, text='{}  {}'.format(df1.at[(i * 4) + j, 'Max Bet2'], df1.at[(i * 4) + j, 'Max Bet2 Casino']),font=("Arial",14))
        l3.place(relx=0.56, rely=0.325, anchor='nw')

        button = Button(frame,text='Expand')
        button.place(relx=0.5,rely=1,anchor='s')

        l4 = Label(frame, text=round(df1.at[(i * 4) + j, 'Arb value'],4),font=('Arial',12,'bold'))
        l4.place(relx=0.5,rely=0.8,anchor='s')

        l5 = Label(frame,text='Arb',font=('Arial',10,'bold'))
        l5.place(relx=0.5,rely=0.625,anchor='s')

    if (i*4)+j == len(df1):
        break

root3 = Tk()
root3.title('{} vs {}'.format(df1.at[0,'Name1'],df1.at[0,'Name2']))
root3.geometry('1860x900')
sf3 = ScrolledFrame(root3)
sf3.pack(expand='yes',fill='both')
sf3.bind_arrow_keys(root3)
sf3.bind_scroll_wheel(root3)
innerf3 = sf3.display_widget(Frame)
frame1 = Frame(innerf3,width=1900,height=475,bd=5)
frame1.pack(side='top')
frame1.pack_propagate(0)


def switch():

    '''if entryA['state']=='disabled':
        entryA['state']='normal'
        entryB['state']='disabled'
    else:
        entryB['state'] = 'normal'
        entryA['state'] = 'disabled'''
    print(radio.get())


radio = IntVar()

gamevs = Label(frame1,text='vs',font=('Arial',40))
gamevs.place(relx=0.5,rely=0,anchor='n')
labelname1 = Label(frame1, text='{}'.format(df1.at[0,'Name1']),font=('Arial',40))
labelname1.place(relx=0.45,rely=0,anchor='ne')
labelname2 = Label(frame1, text='{}'.format(df1.at[0,'Name2']),font=('Arial',40))
labelname2.place(relx=0.55,rely=0,anchor='nw')
fdlabel = Label(frame1,text='fd',font=('Arial',30)).place(relx=0.5,rely=0.175,anchor='n')
dklabel = Label(frame1,text='dk',font=('Arial',30)).place(relx=0.5,rely=0.29,anchor='n')
bmlabel = Label(frame1,text='bm',font=('Arial',30)).place(relx=0.5,rely=0.405,anchor='n')
arb = Label(frame1,text='Arb',font=('Arial',30)).place(relx=0.5,rely=0.55,anchor='n')
arbvalue = Label(frame1,text=round(df1.at[0,'Arb value'],4),font=('Arial',25)).place(relx=0.5,rely=0.64,anchor='n')
ssbutton = Button(frame1, text='Generate Spreadsheet',font=('Arial',15),borderwidth=4).place(relx=0.5,rely=0.75,anchor='n')
calcbutton = Button(frame1, text='Calculate',font=('Arial',15),borderwidth=4).place(relx=0.5,rely=1,anchor='s')

entryB = Entry(frame1, width=6,font=('Arial',20),state='disabled').place(relx=0.535,rely=1,anchor='sw')
radioB = Radiobutton(frame1,variable=radio,value=1,command=switch,text='B',font=('Arial',20)).place(relx=0.585,rely=1,anchor='sw')
entryA = Entry(frame1, width=6,font=('Arial',20)).place(relx=0.465,rely=1,anchor='se')
radioA = Radiobutton(frame1,variable=radio,value=0,command=switch,text='A',font=('Arial',20)).place(relx=0.415,rely=1,anchor='se')



for j in range(3):
    labelbet1 = Label(frame1,text=df1.iat[0,j+1],font=('Arial',30))
    labelbet1.place(relx=0.45,rely=(0.175+(j*0.115)),anchor='ne')
    if labelbet1['text'] == str(df1.at[0,'Max Bet1']):
        labelbet1.configure(relief='groove',borderwidth=4)
    labelbet2 = Label(frame1, text=df1.iat[0, j + 8], font=('Arial', 30))
    labelbet2.place(relx=0.55, rely=(0.175 + (j * 0.115)), anchor='nw')
    if labelbet2['text'] == str(df1.at[0,'Max Bet2']):
        labelbet2.configure(relief='groove',borderwidth=4)




root3.mainloop()
root2.mainloop()

root.mainloop()
