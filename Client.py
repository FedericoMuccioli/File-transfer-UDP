#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import os
import time

IP = socket.gethostbyname(socket.gethostname())
CLIENT_DATA_PATH = "client_data"
PORT = 50000
ADDR = (IP, PORT)
BUF = 4096
DELAY = 0.0001

def handle_server(client, request):
    #split the request in command in "cmd"
    data = request.split(" ", 1)
    cmd = data[0]
    
    #if list, request list to server
    if cmd == "LIST":
        client.sendto(cmd.encode(), ADDR)
        
    #if get, check that there are no files with the same name already in the folder
    #if not request the file from server
    elif cmd == "GET":
        if len(data) != 2 or os.path.sep in data[1]:
            print("Error: enter the name of the file to download")
            return
        filename = data[1]
        filepath = os.path.join(CLIENT_DATA_PATH, filename)
        if os.path.exists(filepath):
            print("Error: file with the same name already present on directory")
            return
        client.sendto(request.encode(), ADDR)
        reply, address = client.recvfrom(BUF)
        reply = reply.decode()
        if (reply != "OK"):
            print(reply)
            return
        try: 
            file = open(filepath, "wb")
            text, address = client.recvfrom(BUF)
            while text:
                file.write(text)
                text, address = client.recvfrom(BUF)
            file.close
        except:
            print("Error: retry the operation")
        
    #if put, verify that the file is valid. If valid upload the file in to the server  
    elif cmd == "PUT":
        if (len(data) != 2):
            print("Error: enter the path of the file to upload")
            return
        path = data[1]
        try:
            file = open(path, "rb")            
        except:
            print("Error: enter the path of a valid file")
            return
        filename = os.path.basename(path)
        request = cmd + " " + filename
        client.sendto(request.encode(), ADDR)
        reply, address = client.recvfrom(BUF)
        if(reply.decode() == "OK"):
            text = file.read(BUF)
            while text:
                client.sendto(text, ADDR)
                text = file.read(BUF)
                time.sleep(DELAY)
            client.sendto(text, ADDR)
        file.close()
        
    #if delete, verify that the file is valid. If valid delete the file in server
    elif cmd == "DELETE":
        if (len(data) != 2):
            print("Error: enter the name of the file to delete")
            return
        client.sendto(request.encode(), ADDR)
        
    #if help, print the server commands
    elif cmd == "HELP":
        client.sendto(cmd.encode(), ADDR)
        
    #else print command not valid and list of valid server commands
    else:
        print("Error: insert a valid comand:")
        client.sendto("HELP".encode(), ADDR)
    
    #print the reply of the server
    reply, address = client.recvfrom(BUF)
    print(reply.decode())
    
#Main function
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #while loop that handles the client's commands. Only ends when the user types Ctrl+C.
    while True:
        request = input("> ")
        handle_server(client, request)


if __name__ == "__main__":
    main()