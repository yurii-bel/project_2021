import sqlite3 as sq

with sq.connect("program.db") as con:
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS User ( 
                User_id INTEGER PRIMARY KEY AUTOINCREMENT,
                Login TEXT NOT NULL,
                Password TEXT NOT NULL       
                 )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS Email (
            Email_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            User_Id INTEGER NOT NULL,
            Email TEXT NOT NULL 
            )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS Telegram (
                Telegram_Id INTEGER PRIMARY KEY AUTOINCREMENT,
                User_Id INTEGER NOT NULL,
                Telegram TEXT NOT NULL 
                )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS Categories (
                Categories_Id INTEGER PRIMARY KEY AUTOINCREMENT,
                User_Id INTEGER NOT NULL,
                Categories TEXT NOT NULL 
                )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS Actions (
                Actions_Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Categories_Id INTEGER NOT NULL,
                Actions TEXT NOT NULL 
                )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS Dates (
                Dates_Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Actions_Id INTEGER NOT NULL,
                Dates TEXT NOT NULL 
                )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS Time (
                Time_Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Actions_Id INTEGER NOT NULL,
                Time TEXT NOT NULL 
                )""")

