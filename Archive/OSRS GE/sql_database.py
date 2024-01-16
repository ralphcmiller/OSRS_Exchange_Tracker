# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 18:54:10 2021

@author: ralph

Handles my personal SQL Database to track OSRS ge items using the OSRS wiki api
"""
import sqlite3
import os
from tabulate import tabulate

def init():
    conn = sqlite3.connect('GEdata.db')
    cur = conn.cursor()
    return conn, cur

def close_db(conn):
    conn.commit()
    conn.close()

def create_table(table):
    conn, cur = init()
    sql = "CREATE TABLE IF NOT EXISTS {}(low real, low_time text, high real, high_time text)"
    cur.execute(sql.format(table))
    close_db(conn)

def get_tables():
    conn, cur = init()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cur.fetchall()
    return table_names
    
def get_data(table):
    conn, cur = init()
    cur.execute("SELECT * FROM {}".format(table))
    data = cur.fetchall()
    return data

def add_data(table, val):
     conn, cur = init()
     sql = "INSERT INTO {} (low, low_time, high, high_time) VALUES (?, ?, ?, ?)"
     cur.execute(sql.format(table), val)
     close_db(conn)

def delete_data():
    delete = input('are you sure you want to delete the entire database? (y/n): ')
    if delete == 'y':
        os.remove('GEdata.db')
        print("Database deleted.")
    else:
        print("Exiting")

def print_data(table):
    x = get_data(table)
    print(table + "\n", tabulate(x, headers=["Sell Price", "Time", "Buy Price", "Time"]))
     
