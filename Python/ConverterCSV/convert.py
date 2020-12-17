# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 11:12:13 2020

@author: juan
"""


import csv
i = 0
aux = {}
with open('ABEV3.csv') as csv_file:
    
    csv_reader = csv.reader(csv_file, delimiter=';')

    csv_reader.__next__()

    for row in csv_reader:
        l = 0
        aux[i] = row[0].split(',"');
        aux[i] = aux[i][:-2]
        for a in aux[i]:
            if(l == 0):
                aux[i][l] = aux[i][l].replace('.', '-')
            aux[i][l] = aux[i][l].replace('"', '')
            aux[i][l] = aux[i][l].replace(',', '.')
            l = l + 1
        i = i + 1
   
import pyodbc

def retornar_conexao_sql():
    server = "DESKTOP-RIUJ6QK"
    database = "bd_base_CS"
    string_conexao = 'Driver={SQL Server Native Client 11.0};Server='+server+';Database='+database+';Trusted_Connection=yes;'
    conexao = pyodbc.connect(string_conexao)
    return conexao.cursor()

i = 0
for a in aux:
    try:
            cursor = retornar_conexao_sql()
            sqlQuery = "INSERT INTO tbl_Candle VALUES ('"+str(aux[i][0])+"', "+str(aux[i][1])+", "+str(aux[i][2])+", "+str(aux[i][3])+", "+str(aux[i][4])+")"
            cursor.execute("SELECT * FROM tbl_Candle WHERE idData = '"+str(aux[i][0])+"'")
            myresult = cursor.fetchall()
            tamanho = len(myresult)
            if tamanho == 0:
                cursor.execute(sqlQuery)
                cursor.commit()
    finally:
        cursor.close
    i += 1
