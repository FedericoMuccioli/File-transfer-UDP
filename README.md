# File-Transfer-UDP 🌐 ![StatusBadge](https://badgen.net/badge/Status/Completed/green)

### File transfer between client and server multithread through UDP protocol

___

## **USAGE**
 1. Run **one instance** of *Server.py*
 2. Run **as many instances** as you want of *Client.py*
  
___

### **COMMANDS AVAIABLE**
*Use this command through the Client instance*
- ***LIST*** prints out the list of files present in the server, located in the “server_data” folder
- ***GET < filename >*** downloads the file, whose name is specified, into the “client_data” folder
- ***PUT < path >*** loads the file, whose path is specified, on the server, in the “server_data” folder
- ***DELETE < filename >*** deletes the file, whose name is specified, from the server, from the “server_data” folder
- ***HELP*** prints out the list of commands that can be delivered to the server
