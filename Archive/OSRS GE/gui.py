# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 18:16:44 2021

@author: ralph
"""

from tkinter import *
import getOSRScopy
import time
from datetime import datetime
import dateutil.relativedelta
import webbrowser



root = Tk()
root.attributes('-topmost',True)
root.iconbitmap("myIcon.ico")
root.title('GE Tracker')


table_lab = Label(root)
low_lab = Label(root)
hi_lab = Label(root)
hitime_lab = Label(root)
lowtime_lab = Label(root)

sell_lab = Label(root)
buy_lab = Label(root)
time_lab = Label(root)

table_lab.grid(row = 0, column = 0)
hi_lab.grid(row = 1, column = 1)
hitime_lab.grid(row = 1, column = 2)
low_lab.grid(row = 2, column = 1)
lowtime_lab.grid(row = 2, column = 2)
sell_lab.grid(row = 1, column = 0)
buy_lab.grid(row = 2, column = 0)
time_lab.grid(row = 0, column = 2)

comment = Button(root, height=3, width=5, text="id", command=lambda: get_input())
comment.grid(row = 0, column = 3)
text_box=Text(root, height=3, width=10)
text_box.grid(row = 0, column = 4)

web_but = Button(root, height=2, text = "see wiki prices",command=lambda: openweb())
web_but.grid(row = 2, column = 4)



def openweb():
    url = "https://prices.runescape.wiki/osrs/item/" + usr
    webbrowser.open(url,1)



def get_input():
    global usr
    usr = text_box.get("1.0","end-1c")

def clock():    
    setup = False    
    itemID = usr
    table, values = getOSRScopy.runScript(itemID, setup)
       
    low = values[0]
    low_time = values[1]  
    hi = values[2]
    hi_time = values[3]
    time_now = time.time()
    
    dt1 = datetime.fromtimestamp(low_time) # 1973-11-29 22:33:09
    dt2 = datetime.fromtimestamp(time_now) # 1977-06-07 23:44:50
    rd = dateutil.relativedelta.relativedelta (dt2, dt1)
    
    low_time = '    {}m  {}s ago'.format(rd.minutes, rd.seconds)
    
    dt1 = datetime.fromtimestamp(hi_time) # 1973-11-29 22:33:09
    dt2 = datetime.fromtimestamp(time_now) # 1977-06-07 23:44:50
    rd = dateutil.relativedelta.relativedelta (dt2, dt1)
    
    hi_time = '    {}m  {}s ago'.format(rd.minutes, rd.seconds)

    print(low, low_time, hi, hi_time)

    table_lab.config(text=table, bg = getOSRScopy.signalChange.x)
    hi_lab.config(text = hi)
    low_lab.config(text = low)
    lowtime_lab.config(text=low_time)
    hitime_lab.config(text=hi_time)
    sell_lab.config(text = 'sell')
    buy_lab.config(text = 'buy')
    time_lab.config(text = 'time')
    
    #lab['text'] = time
    root.after(30000, clock) # run itself again after 1000 ms

# run first time
usr = '554'
getOSRScopy.changes(0)
getOSRScopy.signalChange('grey')
clock()

root.mainloop()