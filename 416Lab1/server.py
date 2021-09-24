'''
ECSE 416: Telecommunication Networks
Experiment 1: A basic Web Sever
-------------------------------------
Group 6
Daniel Astorino 260799820
Lillian Chiu 
'''
# ---------------------------- IMPORTS -----------------------------------------
try:
    import socket
except:
    print("[ERROR] Missing required extension (socket)")

try:
    import sys
except:
    print("[ERROR] Missing required extension (sys)")

# ---------------------------- ARGUMENTS -----------------------------------------
arguments =  sys.argv
host = '127.0.0.1' #localhost
port = arguments[1]      
#response = ""


#Lab Requirement (i): Create a connection socket when contacted by the client 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    #bind socket to specified host and port
    s.bind((host, int(port)))
    #wait for connection
    s.listen(5)
    # connection established
    conn, addr = s.accept()
    print("Connection: OK")
    
    with (conn):
        dataPacket = conn.recv(1024)
        print("Request Message recieved.")

        filename = dataPacket.decode().split(" ")[-1]
        if filename.endswith(".txt"):
            content = "text/html"
        if filename.endswith(".jpg"):
            content = "image/jpg"

        try:
            file = open(filename, 'rb')
        except:
            response = "404 Not found"
            conn.sendall(response.encode()) 
            s.close()
        
        try:
            stream = file.read(1024)
            while (stream):
                print("Sending...")
                conn.send(stream)
                stream = file.read(1024)
            file.close()

            response =  "PUT / HTTP/1.1\r\nServer HTTP Reponse: HTTP 200 OK\r\nContent-Type: " + content
            conn.sendall(response.encode())
            print("Sending complete")
        except:
            response = "500 Not Found"
            conn.sendall(response.encode()) 
            s.close()


        #print('Connected by', addr)

#TODO Add timeout

#404 and 200 doesnt work for images