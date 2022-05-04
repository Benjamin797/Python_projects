import socket
import time

host = ''
port = 5050


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
print("listening...")

try:
    while 1:
        try:

            conn, address = s.accept()
            print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))
            s.setblocking(1)
        except:
            print("[Error accepting connection]")

        conn.send("Hello World".encode())
        data = conn.recv(1024).decode()
        if data:
            print(data)
        time.sleep(1)
except KeyboardInterrupt:
    conn.close()
    pass
