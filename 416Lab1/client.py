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
arguments = sys.argv
host = '127.0.0.1'
port = int(arguments[1])
filename = arguments[2]




#Lab Requirement (i): Create a connection socket to contact the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    print("Connection: OK")

    #Lab Requirement(ii): Send the HTTP request from this connection
    if filename.endswith(".txt"):
        file = open('rx'+ filename, 'w')
        content = "text/html"
        request = "GET / HTTP/1.1\r\nContent-Type:text/html\n " + filename

    if filename.endswith(".jpg"):
        file = open('rx'+ filename, 'wb')
        content = "image/jpg"
        request = "GET / HTTP/1.1\r\nContent-Type:image/jpeg\n " + filename

    s.sendall(request.encode())
    print("Request Message sent.")
    
    #Server gets request and starts sending
    
    data = s.recv(1024)
    while(data):
        print("Recieving...")
        
        #if(data.decode().startswith("404")):
        #    print(data.decode())
        #    break
        
        #if("200" in data.decode()):
        #    break

        if filename.endswith(".txt"):
            file.write(data.decode())
        elif filename.endswith(".jpg"):
            file.write(data)
        data = s.recv(1024)

    file.close()
    print("Server HTTP Reponse: HTTP 200 OK")
    print("Content-Type: " + content)
    
    if content == "text/html":
        file = open('rx'+filename)
        text = file.read()
        print(text)
    
    #print("data packet: ", data.decode())
    print("Socket Closed")


