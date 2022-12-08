import socket
import sys
import os

## Get the name of the file.
def getFileName(data):
    fileName = data.split(' ')[1]
    ## If the file name is '/', change the file name to be index.html.
    if fileName == '/':
        fileName = "/index.html"

    return fileName

## Create the message to send to the client.
def messageToClient(data):
    status = data.split()[2] 
    fileName = getFileName(data)
    path = 'files/files' + fileName

    ## Message we send if the file name is 'redirect'.
    if fileName == '/redirect':
        status += " 301 Moved Permanetly"
        connection = "Connection: close"
        location = "Location: /result.html"
        message = status + '\n' + connection + '\n' + location + '\n\n'
        finalMess = str.encode(message)
    
    ## Check if the file is in the directory.
    elif(fileExist(fileName)):
        ## If the file name is in the directory
        status += " 200 OK"
        connection = data.split('\n')[2].split('\r')[0]
        size = os.path.getsize(path)
        length = "Content-Length: " + (str)(size)
        message = status + '\n' + connection + '\n' + length  + '\n\n'
        finalMess = str.encode(message)
    else:
        ## If the file is not in the directory.
        status += " 404 Not Found"
        connection = "Connection: close"
        message = status + '\n' + connection + '\n\n'
        finalMess = str.encode(message)

    return finalMess
        
## Check if file exists in the directory.
def fileExist(fileName):
    path = 'files/files' + fileName
    return os.path.exists(path)

## Open the specific file according to the name and return it.
def openFile(fileName):
    path = 'files/files' + fileName
    file = None

    if(fileExist(fileName)):
        file = open(path, 'rb')

    return file


## Get data from the command line and check if valid.
args = sys.argv
if(len(args) == 2 and args[1].isnumeric() and (int)(args[1]) in range(0, 65535)):
    port = (int)(args[1])

## Create socket.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', port))
server.listen(5)
client_socket, client_address = server.accept()
client_socket.settimeout(1)

while True:
    try:
        data = client_socket.recv(4096).decode("utf-8")
        ## If the requwst is empty, close the connection and wait for the next client.
        if data == '':
            client_socket.close()
            client_socket, client_address = server.accept()
            client_socket.settimeout(1)
        else:
            # If the end of the message is '\r\n\r\n', 
            # it means the client stops sending the message.
            while not data.endswith('\r\n\r\n'):
                data += client_socket.recv(4096).decode("utf-8")

            print('Received:', data)

            message = messageToClient(data)
            client_socket.send(message)

            fileName = getFileName(data)
            if fileName == '/redirect':
                fileName = '/result.html'

            file = openFile(fileName)
            if file != None:
                client_socket.sendfile(file)
                file.close()
                        
            connection = data.split('\n')[2].split('\r')[0]
            ## Check if the client asks for closing the conncection.
            if connection == "Connection: close":
                client_socket.close()
            # If the connection isn't a keep alive, 
            # close the connection and open a new socket.
            elif connection != "Connection: keep-alive":
                client_socket.close()
                client_socket, client_address = server.accept()
                client_socket.settimeout(1)
    except: 
        # That is, there is a timeout.
        client_socket.close()
        client_socket, client_address = server.accept()
        client_socket.settimeout(1)
