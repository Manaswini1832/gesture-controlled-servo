# -*- coding: utf-8 -*-
import cv2
from cvzone.HandTrackingModule import HandDetector
from numpy import *
from math import *

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon = 0.8, maxHands = 2)

def slope(x1,y1,x2,y2):
    if(x1 == x2) :
        x2 = x2 + (0.001)
    x = (y2 - y1) / (x2 - x1)
    return x


while True :
    success, img = cap.read()
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH )
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT )

    #defining the starting and ending point coordinates of the line segment
    xcoord1 = int(0.3 * width)
    xcoord2 = int(0.75 * width)
    ycoord = int(0.75 * height)
    line_thickness = 40

    #With drawing
    # hands, img = detector.findHands(img) 

    #Without drawing
    hands = detector.findHands(img, draw = False) 


    if (len(hands) == 2) :
        hand1, hand2 = hands[0], hands[1]
        lmList1, lmList2 = hand1["lmList"], hand2["lmList"]
        # Hand1's bottom point
        x1, y1 = lmList1[0][0], lmList1[0][1]
        # Hand1's center
        x2, y2 = hand1["center"][0], hand1["center"][1]
        # Hand2's bottom point
        x3, y3 = lmList2[0][0], lmList2[0][1]
        # Hand2's center
        x4, y4 = hand2["center"][0], hand2["center"][1]

        if((abs(x1 - x3) <= 80) and (abs(x1 - x3) >= -80)) :
            m1 = slope(x1, y1, x2, y2)
            m2 = slope(x1, y1, x4, y4)
            if((1 + (m1 * m2)) == 0) :
                angle1 = 90
            else :
                angle1 = atan((m2 - m1) / (1 + (m1 * m2)))
            angle = round(degrees(angle1))
            if(angle < 0) :
                angle = angle + 180
            # Now draw the lines showing the angle
            ptx = int((x2 + x4) / 2)
            pty = int((y2 + y4) / 2.5)
            cv2.line(img, (x2, y2), (ptx, pty), (255, 0, 0), thickness=1, lineType=8, shift=0)
            cv2.line(img, (ptx, pty), (x4, y4),  (255, 0, 0), thickness=1, lineType=8, shift=0)
            font = cv2.FONT_HERSHEY_SIMPLEX
            string_to_show = str(angle) + " deg"
            cv2.putText(img, string_to_show, (int((x2 + x4) / 2), int((y2 + y4) / 3)), font, 2, (0, 0, 0), 5, cv2.LINE_AA)
        # else :
        #     print("Nah cant get")

    cv2.imshow("Frame", img)
    if cv2.waitKey(1) == ord('q') :
        break