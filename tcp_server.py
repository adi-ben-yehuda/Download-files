import socket
import sys
import os

## Get the name of the file.
def getFileName(data):
    fileName = data.split(' ')[1]
    ## Check if the name file is '/'- we want the index.html file.
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
        ## If the file name is the directory
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
        

# Check if file exist in the directory.
def fileExist(fileName):
    path = 'files/files' + fileName
    return os.path.exists(path)

def openFile(fileName):
    path = 'files/files' + fileName
    file = None
    if(fileExist(fileName)):
        file = open(path, 'rb')
    return file


## Get data from the command line and check if valid.
args = sys.argv
#if(len(args) == 2 and args[1].isnumeric() and (int)(args[1]) in range(0, 65535)):
#  port = (int)(args[1])

## Create socket.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 8080))
server.listen(5)
client_socket, client_address = server.accept()
client_socket.settimeout(1)


while True:
    print("here")
    try:
        data = client_socket.recv(4096).decode("utf-8")
        if data == '':
            client_socket.close()
            client_socket, client_address = server.accept()
            client_socket.settimeout(1)
        else:
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
                        
            
            ## Check if the client ask to close the conncection.
            connection = data.split('\n')[2].split('\r')[0]
            if connection == "Connection: close":
                client_socket.close()
            ## If the connection isn't a keep alive, 
            # close the connection and open a new socket.
            elif connection != "Connection: keep-alive":
                client_socket.close()
                client_socket, client_address = server.accept()
                client_socket.settimeout(1)
    except:
        client_socket.close()
        client_socket, client_address = server.accept()
        client_socket.settimeout(1)

