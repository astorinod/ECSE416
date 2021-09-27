'''
ECSE 416: Telecommunication Networks
Experiment 1: A basic Web Sever
-------------------------------------
Group 6
Daniel Astorino 260799820
Lillian Chiu 260804336
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

try:
    import os
except:
    print("[ERROR] Missing required extension (os)")


# ---------------------------- ARGUMENTS -----------------------------------------
arguments = sys.argv
host = '127.0.0.1'
port = int(arguments[1])
filename = arguments[2]

try:
    timeout = int(arguments[3])
except:
    timeout = 5

response = ""
deleteFile = False

# ----------------------- Communicate with Server ---------------------------------

#Lab Requirement (ii): Client establishes a socket connection to the server
#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(timeout)
s.connect((host, port))
print("Connection: OK")

#Lab Requirement(iii): Send the HTTP request from this connection
if filename.endswith(".txt"):
    file = open('rx'+ filename, 'w', newline='')
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
print("Recieving...")
while(data):
    
    #Check for a HTTP 200 response    
    two = "200"
    if filename.endswith(".txt") and ("200" in data.decode()):
        response = "HTTP 200 OK"
        break
    if filename.endswith(".jpg") and (two.encode('utf-8') in data):
        response = "HTTP 200 OK"
        break
    
    #Check for a HTTP 404 response
    four = "404"
    if filename.endswith(".txt") and ("404" in data.decode()):
        response = "HTTP 404 Not Found"
        deleteFile = True
        break
    if filename.endswith(".jpg") and (four.encode('utf-8') in data):
        response = "HTTP 404 Not Found"
        deleteFile = True
        break
    
    #If the data is not an ERROR or OK reponse, then it's file data. Write it in a new file
    if filename.endswith(".txt"):
        file.write(data.decode())
    elif filename.endswith(".jpg"):
        file.write(data)
    data = s.recv(1024)
file.close()

#If we recieved a 404 error code, make sure no new file is created
if deleteFile and os.path.exists('rx'+ filename):
    os.remove('rx'+ filename)

#Print out the output response, and the file content if the file is a txt
print("Server HTTP Reponse: " + response)

if os.path.exists('rx'+ filename):
    print("Content-Type: " + content)
    if content == "text/html":
        file = open('rx'+filename)
        text = file.read()
        print(text)

try:
    s.close()
    print("Socket Closed")
except:
    print("Closing Socket Failed")


