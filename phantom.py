import cv2, numpy as np, math, time
from graphics import *
from Tkinter import *
from difflib import SequenceMatcher
import time
from tkFileDialog import askopenfilename
import os
import ctypes
import time

root = Tk()
root.configure(background="#a1dbcd")

def callback():
    root.withdraw()

    userInput = T.get("1.0",END)
    keywordsList = userInput.split("\n")
    keywordsList.pop()
    ###Launch client/presentation mode###
    ########################################
    count = len(keywordsList)
    os.system("start " + filename)
    time.sleep(2)
    user32 = ctypes.windll.user32
    F5_KEYWORD = int ("0x74", 16)
    user32.keybd_event(F5_KEYWORD,0,0,0) #is the code for KEYDUP[/code]
    user32.keybd_event(F5_KEYWORD,0,2,0) #is the code for KEYDOWN
    #######################################

    #What slide we are on currently
    wordCount = 0

    counter = 0
    old_count_defects = 0
    check = 0

    vidCap = cv2.VideoCapture(0)

    #Declare constants for keystroke
    FORWARD = int ("0x27", 16)
    BACK = int ("0x26", 16)
    END_SHOW = int ("0x1B", 16)

    while (vidCap.isOpened()):
        ret, img = vidCap.read()
        cv2.rectangle(img, (300,300),(100,510),(0,255,0),0)
        crop_img = img[100:300, 100:300]
        grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        value = (35, 35)
        blurred = cv2.GaussianBlur(grey, value, 0)
        _, thresh1 = cv2.threshold(blurred, 127, 255,
                                   cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        (version, _, _) = cv2.__version__.split('.')

        if version is '3':
            image, contours, hierarchy = cv2.findContours(thresh1.copy(), \
                   cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        elif version is '2':
            contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
                   cv2.CHAIN_APPROX_NONE)

        cnt = max(contours, key = lambda x: cv2.contourArea(x))

        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,100),0)
        hull = cv2.convexHull(cnt)
        drawing = np.zeros(crop_img.shape,np.uint8)
        cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
        cv2.drawContours(drawing,[hull],0,(0,0,255),0)
        hull = cv2.convexHull(cnt,returnPoints = False)
        defects = cv2.convexityDefects(cnt,hull)
        count_defects = 0
        cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            if angle <= 120:
                count_defects += 1
                cv2.circle(crop_img,far,1,[0,0,255],-1)
            #dist = cv2.pointPolygonTest(cnt,far,True)
            cv2.line(crop_img,start,end,[0,255,0],2)
            #cv2.circle(crop_img,far,5,[0,0,255],-1)
        if count_defects == 1:
            if old_count_defects != count_defects:
                counter = 0
            old_count_defects = 1
            counter += 1
            if counter > 30 and check == 0:
                counter = 0
                check = 1
                user32.keybd_event(FORWARD,0,0,0) #is the code for KEYDUP
                user32.keybd_event(FORWARD,0,2,0) #is the code for KEYDOWN
                print("1")

        elif count_defects == 2:
            if old_count_defects != count_defects:
                counter = 0
            old_count_defects = 2
            counter += 1
            if counter > 30 and check == 0:
                counter = 0
                check = 1
                user32.keybd_event(BACK,0,0,0) #is the code for KEYDUP
                user32.keybd_event(BACK,0,2,0) #is the code for KEYDOWN
                print("2")


        elif count_defects == 3:
            if old_count_defects != count_defects:
                counter = 0
            old_count_defects = 3
            counter += 1
            if counter > 30 and check == 0:
                counter = 0
                check = 1
                user32.keybd_event(END_SHOW,0,0,0) #is the code for KEYDUP
                user32.keybd_event(END_SHOW,0,2,0) #is the code for KEYDOWN
                print("3")

        elif count_defects == 4:
            if old_count_defects != count_defects:
                counter = 0
            old_count_defects = 4
            counter += 1
            if counter > 30 and check == 0:
                counter = 0
                check = 1

                print("4")

        else:
            if old_count_defects != count_defects:
                counter = 0
            old_count_defects = 0
            check = 0
        #cv2.imshow('drawing', drawing)
        #cv2.imshow('end', crop_img)
        all_img = np.hstack((drawing, crop_img))
        cv2.imshow('Contours', all_img)

        k = cv2.waitKey(10)
        if k == 27: #ASCII key for esc char
            break

root.withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)

root.deiconify()
w = Label(root, text="Please write your keywords according to the order of your slides (new lines indicate new slide/bullet)")
root.title("Phantom")
root.geometry("550x350")
T = Text(root, height=15, width=50)
b = Button(root, text="Launch my document and slideshow", command=callback)

w.pack(side="top", fill = "both",expand=False, padx=4, pady=4)

b.pack(side="bottom", expand=True, padx=4, pady=4)

T.pack(side="top", expand=False, padx=4, pady=4)



root.mainloop()
