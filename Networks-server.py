#!/usr/bin/env python
# coding: utf-8

# In[1]:


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

os.chdir(r'C:/Data files/01- Aya/College/Semester 8/Computer Networks/Projects/Project 1/Server directory')


# In[2]:


def Splitter(String, delimiter):
    Splitted = String.split(delimiter)
    return Splitted

def bArraySplitter(byteArr):
    delim = "\\n\\n".encode()
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


# In[3]:


lock = threading.Lock() 
def Server_Handler(String):
    String = bArraySplitter(String)
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
        exists = os.path.isfile('C:/Data files/01- Aya/College/Semester 8/Computer Networks/Projects/Project 1/Server directory' + request[1])
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
        
        
        
        


# In[4]:


#function 
def parseHTTP(portNum): 
    # data received from client 
    dt = portNum.recv(2048)
    data = bytearray(dt)
    while dt:
        dt = portNum.recv(2048)
        if dt:
            dt = bytearray(dt)
            data.extend(dt)

    #handle client request 
    #response is a bytearray
    response = Server_Handler(data)
    print(data)
    
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


int(30/4)


# In[2]:


img = open("988324_447936958650207_233660448_n.jpg", "rb")
img = img.read()
file = bytearray(img)
print(file)
response = 'HTTP/1.0 200 ok\nDate: 5/8/2019\n\n'
response = bytearray(response.encode())
response.extend(file)


# In[ ]:


delim = "\n\n".encode()
delim = bytearray(delim)
retFile = response.split(delim, 1)
i=2
r = retFile[1]
print(r)
retFile = retFile[0].decode()
print(retFile)


# In[ ]:


import io
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
image = Image.open(io.BytesIO(r))
image.save('aya.jpg')


# In[ ]:


from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen('https://en.wikipedia.org/wiki/Peter_Jeffrey_(RAAF_officer)')
bs = BeautifulSoup(html, 'html.parser')
images = bs.find_all('img', {'src':re.compile('.jpg')})
for image in images: 
    print(image['src']+'\n')


# In[ ]:


x = 'GET /links.txt HTTP/1.0\\nfjhnewkm\\n\\n'
x = x.encode()
print(x)
x = bytearray(x)
print(x)
y = bArraySplitter(x)
print(len(y))
print(y[0])


# In[ ]:


aya = 'a' + 'a'
print(aya)


# In[ ]:


filename = 'aya'
filedata = "kjhkjhbkjbkjbkjbkjb"
file  = open(filename[1:], “w”)
file.write(filedata)
file.close()


# In[ ]:


file = open(filename[1:],"r")
file = file.read()
file = file.encode()
file = bytearray(file)

if (len(response) > 2048):
        print(response)
        j = int( len(response)/2048)
        print(j)
        #divide into several bytearrays
        for i in range (0, j*2048, 2048):
            chunk = response[i:i+2048]
            print(chunk)
            portNum.send(chunk)
        k = len(response) - j*2048
        print(k)
        chunk = response[-k:]
        portNum.send(chunk)
    else:
        portNum.send(response)


# In[ ]:


#if (len(response) > 2048):
 #       print(response)
  #      j = int( len(response)/2048)
   #     print(j)
        #divide into several bytearrays
    #    for i in range (0, j*2048, 2048):
     #       chunk = response[i:i+2048]
      #      print(chunk)
       #     portNum.send(chunk)
        #k = len(response) - j*2048
        #print(k)
        #chunk = response[-k:]
        #portNum.send(chunk)
    #else:
    #portNum.send(response)

