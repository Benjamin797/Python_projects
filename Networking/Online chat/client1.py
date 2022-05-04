import socket

host = socket.gethostbyname(socket.gethostname())
port = 5050
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print("Binding at port : " + str(port))
try:
    print("Connection established at : " + s.recv(1024).decode("utf-8"))

except:
    print("No connected...")

while True:
    try:
        cmd = input(">>")
        if cmd == 'quit':
            s.send(str.encode(cmd))
            break

        if len(str.encode(cmd)) > 0:
            s.send(str.encode(cmd))
            server_resp = s.recv(1024).decode("utf-8")
            print(server_resp, end="")

    except:
        print("[Error sending commands]...")


print("Disconnect...")
s.close()
