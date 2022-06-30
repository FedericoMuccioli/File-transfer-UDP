# File-transfer-UDP
File transfer between client and server multithread through UDP protocol

Execution:
Launch both applications, Server.py and Client.py. From the client interface it will be possible to issue various orders for server management, in more detail:

-LIST prints out the list of files present in the server, located in the “server_data” folder.

-GET <filename> downloads the file, whose name is specified, into the “client_data” folder.

-PUT <path> loads the file, whose path is specified, on the server, in the “server_data” folder.

-DELETE <filename> deletes the file, whose name is specified, from the server, from the “server_data” folder.

-HELP prints out the list of commands that can be delivered to the server.
