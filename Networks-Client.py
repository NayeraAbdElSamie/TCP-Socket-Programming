#!/usr/bin/env python
# coding: utf-8

# In[1]:


def Splitter(String, delimiter):
    Splitted = String.split(delimiter)
    return Splitted

def bArraySplitter(byteArr):
    delim = "\n\n".encode()
    delim = bytearray(delim)
    retFile = byteArr.split(delim, 1)
    return retFile


# In[ ]:


from socket import *
from PIL import Image
import io
import os

os.chdir(r'D:\College\8th term\Computer Networks\Lab\Files')

serverName = '192.168.43.58'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
print(clientSocket)
request = input("Enter your request: ")

Splitted_request = Splitter(request, '\n')
request_line = Splitter(Splitted_request[0], ' ')
file_type = request_line[1].split(".")

if (request_line[2] == "HTTP/1.0"):
    version = 0
else:
    version = 1
    
if(request_line[0] == "GET"):
    clientSocket.send(request.encode())
    dt = clientSocket.recv(2048)
    data = bytearray(dt)
    while dt:
        dt = clientSocket.recv(2048)
        if (dt):
            dt = bytearray(dt)
            data.extend(dt)

    response = data

    return_file = bArraySplitter(response)

    response = return_file[0].decode()
    file = Splitter(response, '\n')
    print('\n\n')
    print(file)
    file_type = Splitter(file[2], ' ')

    if (file_type[1] == "txt"):
        filename = request_line[1]
        f = open(filename[1:], 'w')
        f.write(return_file[1].decode())
        f.close()
    elif (file_type[1] == "jpg"):
        imgname = request_line[1]
        image = Image.open(io.BytesIO(return_file[1]))
        image.save(imgname[1:])
    else:
        print("HTML")
    
elif(request_line[0] == "POST"):

    if (file_type[1] == "html"):
        filename = request_line[1]
        file = open(filename[1:], "r")
        file = file.read()
        file = file.encode()
        file = bytearray(file)
        filetype = "text/html"
    if (file_type[1] == "jpg"):
        imgname = request_line[1]
        img = open(imgname[1:], "rb")
        img = img.read()
        file = bytearray(img)
    if (file_type[1] == "txt"):
        filename = request_line[1]
        file = open(filename[1:], "r")
        file = file.read()
        file = file.encode()
        file = bytearray(file)

    length = len(file)
    #request = 'POST' + request_line[1] + ' HTTP/1.' + str(version) + Splitted_request[1] + Splitted_request[2] + '\nContent-Type: ' + file_type[1] + '\nContent-Length: ' + str(length) + '\n\n'
    request = bytearray(request.encode())
    request.extend(file)
    clientSocket.send(request)
else:
    print("Invalid request")

clientSocket.close()


# In[ ]:




