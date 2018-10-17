#! /usr/bin/env python3



import socket, sys, re, os
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(5)
# s is a factory for connected sockets
print("Ready to connect")

#First we are gonna wait for the file name
while 1:
    conn, addr = s.accept()
    pid = os.getpid()
    if not os.fork():
        print("new child process handling connection from", addr)
        print("waiting for filename\n")
        filename = conn.recv(100).decode()
        if filename:  # this will be use to make sure that at least the length of the file is receive
            if len(filename.split()) < 2:
                filename = filename + conn.recv(100).decode()
            MessageLength = int(filename.split()[0])
            while len(filename) < MessageLength:
                filename = filename + conn.recv(1024).decode()  # This is use to make sure the entire message is receive
            filename = filename[len(str(filename.split()[0]))+1:]   # This is to remove the header from the file name
            if os.path.exists(filename):
                conn.send("X".encode())  # keeping the handshake simple, an X if file found and a O if file not stored
                continue
            else:
                conn.send("O".encode())  # Server is ready to receive
            print("File name receive staring download ")
            print(filename)
            IncomingFile = open(filename, "w")
            IncomingPacket = conn.recv(100).decode()
            MessageLength = int(IncomingPacket.split()[0])

            while IncomingPacket != "-1":  # if -1 is receive it means the file is over
                try:
                    while len(IncomingPacket) != MessageLength or len(IncomingPacket) < MessageLength :
                        IncomingPacket = IncomingPacket + conn.recv(100).decode()  # This will check the message is send compelatly
                    IncomingPacket = IncomingPacket[len((IncomingPacket.split()[0])):]
                    IncomingFile.write(IncomingPacket)
                    conn.send("R".encode())  # Send R if the message was receive
                    IncomingPacket = conn.recv(100).decode()
                    if IncomingPacket.split()[0] == "-":
                        break
                    MessageLength = int(IncomingPacket.split()[0])

                except s.timeout:
                    conn.send("M".encode())  # Send M if there was a error
                    IncomingPacket = conn.recv(100).decode()  # Start the process again

            IncomingFile.close()
            print("Download Completed")

