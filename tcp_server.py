import socket
import sys
import os



def printFile(fileName):
    dataLine = ''
    path = 'files/files' + fileName
    file = open(path, 'r')
    line = file.readline()
    while line:
        if (len(line.split('<u>')) > 1):
            dataLine += (str)(line.split('<u>')[1]).split('</u>')[0]

        line = file.readline()

    file.close()
    return dataLine

def messageToClient(data):
    status = data.split()[2]
    fileName = data.split(' ')[1]
    if fileName == '/':
        fileName = "/index.html"
    
    if(fileExist(fileName)):
        if fileName == 'redirect':
            status += " 301 Moved Permanetly"
            connection = "Connection: close"
            location = "Location: /result.html"
            message = status + '\n' + connection + '\n' + location + '\n\n'
        else:
            status += " 200 OK"
            connection = data.split('\n')[2].split('\r')[0]
            contentFile = printFile(fileName)
            length = "Content-Length: " + (str)(len(contentFile))
            message = status + '\n' + connection + '\n' + length  + '\n\n' + contentFile
    else:
        status += " 404 Not Found"
        connection = "Connection: close"
        message = status + '\n' + connection + '\n\n'

    return message
        


def fileExist(fileName):
    path = 'files/files' + fileName
    return os.path.exists(path)
    


## Get data from the command line and check if valid.
args = sys.argv
#if(len(args) == 2 and args[1].isnumeric() and (int)(args[1]) in range(0, 65535)):
#  port = (int)(args[1])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 8080))
server.listen(5)

while True:
    client_socket, client_address = server.accept()
    print('Connection from: ', client_address)
    data = client_socket.recv(100)
    print('Received:', data)
    dataStr = data.decode("utf-8")
    client_socket.send(str.encode(messageToClient(dataStr)))
    client_socket.close()
    print('Client disconnected')