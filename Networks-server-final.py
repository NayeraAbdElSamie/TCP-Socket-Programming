#!/usr/bin/env python
# coding: utf-8

# In[6]:


import os
import io
import urllib.request as urllib2
import threading
import time
import time
from socket import *
from _thread import *
from PIL import Image 
from bs4 import BeautifulSoup
from datetime import datetime

os.chdir(r'D:/College/8th term/Computer Networks/Lab/Server files')


# In[7]:


def Splitter(String, delimiter):
    Splitted = String.split(delimiter)
    return Splitted

def bArraySplitter(byteArr, delimiter):
    delim = delimiter.encode()
    delim = bytearray(delim)
    retFile = byteArr.split(delim, 1)
    return retFile
    
def File_Type (file):
    file_type = file.split(".")
    if (file_type[1]=="html"):
        return 0, file_type[1]
    if (file_type[1]=="jpg" or file_type[1]=="png" or file_type[1]=="tif" or  file_type[1]=="gif" or file_type[1]=="jpeg"):
        return 1, file_type[1]
    if (file_type[1]=="txt"):
        return 2, file_type[1]  


# In[8]:


lock = threading.Lock() 
def Server_Handler(String):
    String = bArraySplitter(String, '\\n\\n')
    print(String[0])
    header = String[0].decode()
    req = Splitter(header, '\n')
    print(req)
    request = Splitter(req[0], ' ')
    
    if (request[2] == "HTTP/1.0"):
        version = '0'
    else:
        version = '1'
    
    if (request[0] == "GET"):
        exists = os.path.isfile('D:/College/8th term/Computer Networks/Lab/Server files' + request[1])
        if(exists):
            x, filetype = File_Type(request[1])
            if (x==0):
                filename = request[1]
                file = open(filename[1:],"r")
                file = file.read()
                file = file.encode()  
                file = bytearray(file)
                filetype = "text/html"        
            if (x==1):
                imgname = request[1]
                img = open(imgname[1:], "rb")
                img = img.read()
                file = bytearray(img)
            if (x==2):
                filename = request[1]
                # lock acquired by client
                lock.acquire()
                file = open(filename[1:],"r")
                file = file.read()
                # lock released after operating on specified image/file/html 
                lock.release()
                file = file.encode()
                file = bytearray(file)
     
            length = len(file)
            date = datetime.now()
            date = date.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
            response = 'HTTP/1.' + version + ' 200 OK\nDate: ' + date + '\nContent-Type: ' + filetype + '\nContent-Length: ' + str(length) + '\n\n'
            response = bytearray(response.encode())
            response.extend(file)
        else:
            response = 'HTTP/1.' + version + ' 404 Not found'
            response = bytearray(response.encode())

    elif (request[0] == "POST"):
        response = request[2] + " 200 OK"
        response = bytearray(response.encode())
        x, filetype = File_Type(request[1])
        if (x==0):
            print("this is a html file")
            #some function for html files
        if (x==1):
            imgdata = String[1]
            imgname = request[1]
            image = Image.open(io.BytesIO(imgdata))
            image.save(imgname[1:])
        if (x==2):
            filedata = String[1].decode()
            filename = request[1]
            file  = open(filename[1:], 'w')
            file.write(filedata)
            file.close()
    
    return response


# In[9]:


#function 
def parseHTTP(portNum): 
    # data received from client 
    dt = portNum.recv(2048)
    
    inst = bArraySplitter(dt, ' ')
    
    decoded_dt = inst[0].decode()
    #inst = Splitter(decoded_dt, ' ')
    
    if (decoded_dt == 'GET'):
        data = bytearray(dt)
        #handle client request 
        #response is a bytearray
        response = Server_Handler(data)
        portNum.send(response)
        
    elif (decoded_dt == 'POST'):
        data = bytearray(dt)
        while dt:
            dt = portNum.recv(2048)
            if (dt):
                dt = bytearray(dt)
                data.extend(dt)
        #handle client request 
        #response is a bytearray
        response = Server_Handler(data)
        portNum.send(response)
  
    # connection closed 
    portNum.close() 


# In[ ]:


serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(2)
print('The server is ready to receive')

while 1:
    portNum, IP = serverSocket.accept()
    print('Connected to :', IP, ':', portNum)
     
    # Start a new thread and return its identifier 
    start_new_thread(parseHTTP, (portNum,)) 
    
serverSocket.close()


# In[ ]:




