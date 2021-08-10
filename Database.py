import sqlite3 as sqlite
import pandas as pd
import pyAesCrypt
import os

def create_database(conn):
    cursor = conn.cursor()

    cursor.execute(""" CREATE TABLE ServingOfficers 
                    (SNO NUM ,IC TEXT, DOB TEXT , NAME TEXT ,RANK TEXT ,EMAIL TEXT,MOBILE NUM ,ADDRESS TEXT)""")

    cursor.execute(""" CREATE TABLE RetiredOfficers 
                    (SNO NUM ,IC TEXT, DOB TEXT , NAME TEXT ,RANK TEXT ,EMAIL TEXT,MOBILE NUM ,ADDRESS TEXT)""")

    wb1 = pd.read_excel('./Database/Serving Officers.xlsx')
    wb2 = pd.read_excel('./Database/Retired Officers.xlsx')

    wb1.to_sql('ServingOfficers', conn, if_exists='append', index=False)
    wb2.to_sql('RetiredOfficers', conn, if_exists='append', index=False)


def encrypt_database() :
    password = "bits-pilani"
    pyAesCrypt.encryptFile("./Database/Mydatabase.db",
                           "./Database/Mydatabase.aes", password)


def decrypt_database() :
    password = "bits-pilani"
    pyAesCrypt.decryptFile("./Database/Mydatabase.aes",
                           "./Database/Mydatabase.db", password)



