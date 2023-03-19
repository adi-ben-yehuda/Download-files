# network_ex2
# Chat

## Introduction
In this project, we would like to implement a simple chat using UDP Protocol. Our chat will behave in a similar way to a WhatsApp group, where any member of the group can write, and every message someone writes is sent to all members of the group. Please note, when someone sends a message to the group - the message is sent to the server immediately. However, the server will send the appropriate messages to clients only when they contact the server.

## Table of contents
* [General Information](#general-information)
* [Installation](#installation)
* [Project status](#project-status)
* [Contact](#Contact)


## General Information
This project implements a TCP server that functions as follows: The client sends to the server the name of a file he wishes to download from (that is, for the server to send back to him).
The files are located in a folder named files which is in the same folder where the server is located. The file name can also include a path. That is, if the client sent only the name of the file, then the file should be inside the files folder at the top level. If the file name also contains a folder path, the server searches for the file according to the path inside the files folder.
The format in which the client sends to the server is the following format: in the first line it says: GET [file] HTTP/1.1
When instead of [file] the name of the file will be written.
We will specify that if the name of the file is a single character / (slash), then it means the file named: index.html

The client has finished sending the message when it sends a new line twice, i.e. \r\n\r\n
If the file exists, the server will return:

~~~~
HTTP/1.1 200 OK
Connection: [conn]
Content-Length: [length]
~~~~

Then a blank line, then the contents of the file.
When, instead of [conn] the value of the connection field that appeared in the client's request will be listed, and instead of [length] the size of the sent file will appear. Note, length is the number of bytes that are actually sent.
For example, the client sent:

~~~~
GET / HTTP/1.1
…
Connection: close
…
~~~~





## Installation
Before installing this project, you need to install on your computer:
* Git

After it, run the following commands in the terminal:

```
git clone https://github.com/adi-ben-yehuda/Chat.git
```
Run the server:
```
python server.py port
```
For example: 
```
python server.py 12345
```
Open new terminals for the clients and run the following command:

```
python client.py ip port
```
For example: 
```
python client.py 127.0.0.1 12345
```
## Project status 
The project is in the beginning stages and will develop over time.

## Contact
Created by @adi-ben-yehuda and @ShaharMosh - feel free to contact us!
