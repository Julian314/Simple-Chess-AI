import sqlite3
from sqlite3 import Error
from create_connection import create_connection

def create_table_dataset(conn):

    sql_create_shessgames_table = """ CREATE TABLE IF NOT EXISTS dataset (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                        binary blob,
                                        eval float
                                    );"""
    try:
        c = conn.cursor()
        c.execute(sql_create_shessgames_table)
    except Error as e:
        print(e)

def create_table_shessgames(conn):
    sql_create_shessgames_table = """ CREATE TABLE IF NOT EXISTS dataset (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                        fen text,
                                        binary blob,
                                        white_elo int,
                                        black_elo int,
                                        eval float
                                    );"""
    try:
        c = conn.cursor()
        c.execute(sql_create_shessgames_table)
    except Error as e:
        print(e)    

conn = create_connection("shess_dataset.db")
create_table_dataset(conn)

