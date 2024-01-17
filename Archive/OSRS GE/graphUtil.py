# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 21:59:05 2021

@author: ralph
"""
import sql_database
import matplotlib.pyplot as plt
from dateutil import parser
from matplotlib import style
style.use('fivethirtyeight')

def graph_data(table):
    conn, cur = sql_database.init()
    cur.execute('SELECT low_time, low FROM {}'.format(table))
    
    data = cur.fetchall()
    
    dates = []
    values = []
    
    for row in data:
        dates.append(parser.parse(row[0]))
        values.append(row[1])

    ###########################################################
    cur.execute('SELECT high_time, high FROM {}'.format(table))
    
    data = cur.fetchall()
    
    dates1 = []
    values1 = []
    
    for row in data:
        dates.append(parser.parse(row[0]))
        values.append(row[1])
        
    return dates, values

