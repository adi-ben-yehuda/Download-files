import socket
import sys
import os



def printFile(fileName):
    path = 'files/files' + fileName
    file = open(path, 'r')
    line = file.readline()
    while line:
        if (len(line.split('<u>')) > 1):
            dataLine = (line.split('<u>')[1]).split('</u>')[0]
            print(dataLine)

        line = file.readline()

    file.close()

    
    


## Get data from the command line and check if valid.
args = sys.argv
#if(len(args) == 2 and args[1].isnumeric() and (int)(args[1]) in range(0, 65535)):
#  port = (int)(args[1])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 8081))
server.listen(5)

while True:
    client_socket, client_address = server.accept()
    print('Connection from: ', client_address)
    data = client_socket.recv(100)
    print('Received:', data)
    dataStr = data.decode("utf-8")
    fileName = (str)(dataStr).split(' ')[1]
    printFile(fileName)
    client_socket.send(data.upper())
    client_socket.close()
    print('Client disconnected')