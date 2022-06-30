#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
import threading
import time

IP = socket.gethostbyname(socket.gethostname())
SERVER_DATA_PATH = "server_data"
PORT = 50000
ADDR = (IP, PORT)
BUF = 4096
DELAY = 0.0001

#Function that handles all the commands of client
def handle_client(server, request, addr):
    #split the request in command in "cmd"
    request = request.decode()
    print("\n" + request)
    data = request.split(" ", 1)
    cmd = data[0]
    
    #if command is LIST 
    if cmd == "LIST":
        #check if directory not empty.
        #if not put in reply names files in directory SERVER_DATA_PATH
        files = os.listdir(SERVER_DATA_PATH)
        if len(files) == 0:
            reply = "The server directory is empty"
        else:
            reply = "\n".join(f for f in files)
            
    #if command is GET
    elif cmd == "GET":
        #join the filename with the path and check if exists the file
        filename = data[1]
        path = os.path.join(SERVER_DATA_PATH, filename)
        #the file exists, send the file to client
        if (os.path.exists(path)):
            try:
                file = open(path, "rb")
                server.sendto("OK".encode(), addr)
                text = file.read(BUF)
                while text:
                    server.sendto(text, addr)
                    text = file.read(BUF)
                    time.sleep(DELAY)
                server.sendto(text, addr)
                file.close()
                reply = "File downloaded successfully"
            except:
                reply = "Error: retry the operation"
        #file doesn't exist, send the error message to client.
        else:
            reply = "Error: file not found"

    #if command is PUT
    elif cmd == "PUT":
        #check if file to upload already exists, if not creates the file
        filepath = os.path.join(SERVER_DATA_PATH, data[1])
        if (os.path.exists(filepath)):
            reply = "Error: file with the same name already present on database"
            server.sendto("Error".encode(), addr)
        else:
            server.sendto("OK".encode(), addr)
            try:
                file = open(filepath, "wb")
                text, addr = server.recvfrom(BUF)
                while text:
                    file.write(text)
                    text, addr = server.recvfrom(BUF)
                file.close()
                reply = "File uploaded successfully"
            except:
                reply = "Error: retry the operation"
            
    #if command is DELETE
    elif cmd == "DELETE":
        ##check if file to delete exists, if not send error message
        files = os.listdir(SERVER_DATA_PATH)
        filename = data[1]
        if len(files) == 0:
            reply = "Error: the server directory is empty"
        else:
            if filename in files:
                path = os.path.join(SERVER_DATA_PATH, filename)
                if (os.system(f'rm "{path}"') == 0):
                    reply = "File deleted successfully"
                else:
                    reply = "File not deleted"
            else:
                reply = "Error: file not found"
                
    #if command is HELP
    elif cmd == "HELP":
        #send commands list
        reply = "LIST: List all the files from the server\n"
        reply += "PUT <path>: Upload a file to the server\n"
        reply += "GET <filename>: Download a file from the server\n"
        reply += "DELETE <filename>: Delete a file from the server\n"
        reply += "HELP: List all the commands"

    #send reply to client and print the result in server
    print(reply)
    server.sendto(reply.encode(), addr)

#Main function
def main():
    #Start the server and create the socket
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(ADDR)
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    #While loop that recives the request from the client.
    #When a request is received, a new thread is created to handle the request.
    while True:
        request, addr = server.recvfrom(BUF)
        thread = threading.Thread(target=handle_client, args=(server, request, addr))
        thread.start()
        thread.join()
        

if __name__ == "__main__":
    main()