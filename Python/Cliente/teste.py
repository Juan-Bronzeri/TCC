# -*- coding: utf-8 -*-
import pyodbc
import zmq

myresult = 0
horaAtual = "00"
dataAtual = "00"

def retornar_conexao_sql():
    server = "DESKTOP-RIUJ6QK"
    database = "bd_base_CS"
    string_conexao = 'Driver={SQL Server Native Client 11.0};Server='+server+';Database='+database+';Trusted_Connection=yes;'
    conexao = pyodbc.connect(string_conexao)
    return conexao.cursor()

def remote_send(socket, data):
    try:
        socket.send_string(data)
        msg = socket.recv_string()
        return (msg)
    except zmq.Again as e:
        print ("Waiting for PUSH from MetaTrader 5.."+e)
        
# Get zmq context
context = zmq.Context()

# Create REQ Socket
reqSocket = context.socket(zmq.REQ)
reqSocket.connect("tcp://localhost:5555")

while(True):
    # Send RATES command to ZeroMQ MT4 EA
    petr4 = remote_send(reqSocket, "COMPRA")
    petr4 = remote_send(reqSocket, "RATES|ABEV3")
    petr4 = petr4.split(",")
    petr4[0] = petr4[0].replace('-', ' ')
    petr4[0] = petr4[0].replace('.', '-')
    if (int(petr4[0][8]) != int(horaAtual[0]) | int(petr4[0][9]) != int(horaAtual[1])):
        try:
            horaAtual = petr4[0][8] + petr4[0][9]
            cursor = retornar_conexao_sql()
            data = petr4[0]
            data = data[:-6]
            sqlQuery = "INSERT INTO tbl_Candle VALUES ('"+str(data)+"', "+str(petr4[1])+", "+str(petr4[2])+", "+str(petr4[3])+", "+str(petr4[4])+")"
            cursor.execute("SELECT * FROM tbl_Candle WHERE idData = '"+str(data)+"'")
            myresult = cursor.fetchall()
            tamanho = len(myresult)
            if tamanho == 0:
                cursor.execute(sqlQuery)
                cursor.commit()
        finally:
            cursor.close
    if(int(dataAtual[0]) != int(petr4[0][8]) | int(dataAtual[1]) != int(petr4[0][9])): 
        dataAtual = petr4[0][8] + petr4[0][9]
        abertura = petr4[1]