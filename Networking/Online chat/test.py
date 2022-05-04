
import threading
'''
import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")
'''
fn = ['upload', 'download', 'keylog', 'screenshot', 'webcam']

c = input(">>")
def chercher(c, fn):
    id = True
    for i in fn:

        if c == i:
            id = True
            break
        else:
            id = False


    return id

print(chercher(c,fn))