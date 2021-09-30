'''
ECSE 416: Telecommunication Networks
Experiment 1: A basic Web Server
-------------------------------------
Group 6
Daniel Astorino 260799820
Lillian Chiu 260804336
'''
# ---------------------------- IMPORTS -----------------------------------------


try:
    import socket #library to create socket
except:
    print("[ERROR] Missing required extension (socket)")

try:
    import sys
except:
    print("[ERROR] Missing required extension (sys)")

try:
    import os
except:
    print("[ERROR] Missing required extension (os)")


# ---------------------------- ARGUMENTS -----------------------------------------
arguments =  sys.argv
host = '127.0.0.1' #localhost
port = int(arguments[1])
# command line arguments start at 0

exists = True


# ----------------------- Communicate with Client ---------------------------------

#Lab Requirement (i): Server is launched to listen to a localhost port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, int(port)))       #bind socket with a given host and port
s.listen(5)                     #listen for a connection 
conn, addr = s.accept()         #connection is established
print("Connection: OK")


with (conn): # dont need to manually close the socket
# will close the socket when the program stops running (ex: if theres an error)
    
    #Lab Requirement (iii): Server receives an HTTP request from this connection 
    dataPacket = conn.recv(1024)
    print("Request Message recieved.")

    #Lab Requirement (iv): Request is parsed to determine path of a file being requested
    filename = dataPacket.decode().split(" ")[-1]
    
    #We check the file type to determine the content type of the file
    if filename.endswith(".txt"):
        content = "text/html"
    if filename.endswith(".jpg"):
        content = "image/jpg"

    #Lab Requirement (v): Server gets the requested file from the server's file system 
    try:
        file = open(filename, 'rb')
    except:
        #If the file does not exist in the server directory, send a 404 error response
        response = "404 Not found"
        exists = False
        conn.sendall(response.encode()) 
        s.close()
    
    #If the file exists we begin sending it to the client, packet by packet
    if exists:
        try:
            stream = file.read(1024)
            print("Sending...")
            while (stream):
                conn.send(stream)
                stream = file.read(1024)
            file.close()
            
            #Lab Requirement (vi): Server creates an HTTP response message incorporating a content of the 
            #                      requested file preceded by header lines, including a responding code
            response =  "PUT / HTTP/1.1\r\nServer HTTP Reponse: HTTP 200 OK\r\nContent-Type: " + content
            #Lab Requirement (vii): Server sends the response to the client
            conn.sendall(response.encode())
            print("Sending complete")
        except:
            response = "500 Not Found"
            conn.sendall(response.encode()) 
            s.close()

s.close()
