# imports
import pygame
import sqlite3
import sys
import os

# SQL variables
con = sqlite3.connect('test_db')
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS test_db")
print('Test Table Dropped')

cur.execute("CREATE TABLE IF NOT EXISTS test_db (usr_id PRIMARY KEY, usr_nm TEXT)")
print('Test Table Created')
con.commit()


cur.execute("INSERT INTO test_db (usr_nm, usr_id) VALUES (?, 1)")
print('Inserted into usr_nm')
con.commit()


print('List of Tables:')
os.system('litecli -D test_db -e .tables')

print('List of Databases:')
os.system('litecli -D test_db -e .databases')

print('Selected:')
os.system('litecli -D test_db -e "select * from test_db"')