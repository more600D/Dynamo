# -*- coding: utf-8 -*-
import sqlite3

db = "C:\\Users\\s.shvydko\\Desktop\\ModelLocationTable.db3"
con = sqlite3.connect(db)

cur = con.cursor()

table_list = cur.execute("SELECT ModelNormalizedPath FROM ModelStorageTable")
for model in table_list:
    if '002_ilmensky' in str(model):
        print(model)
