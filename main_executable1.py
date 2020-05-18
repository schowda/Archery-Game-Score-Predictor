##importing all the dependencies***********************************
import cv2
import numpy as np
from searching import npsearch
from scipy.spatial import distance
from masking import imgmask
import time
import os
from tkinter import *
import datetime

player = "Player 1"
##filling all the necessary values***********************************
threshold = 40
red_low = 190
red_high = 220
'''radius of all the circles in pixels from the center.
calculated using (480/max_radius_length in mm)x(radius_of_the_circle_to_draw in mm)'''
r1 = 17
r2 = 33
r3 = 55
r4 = 77
r5 = 97
r6 = 117
r7 = 138
r8 = 159

# r1 = 10
# r2 = 20
# r3 = 33
# r4 = 44
# r5 = 55
# r6 = 67
# r7 = 78
# r8 = 92
score = []

l1score=0
l2score=0
l3score=0
found_dist=0
check = 0

cap = cv2.VideoCapture(1)
width = cap.get(3)
height = cap.get(4)

##functions to be used*******************************************
def draw_circle(img):
    img = cv2.circle(img,(int(width/2),int(height/2)),r1,(255,255,255),1)
    img = cv2.circle(img,(int(width/2),int(height/2)),r2,(255,255,255),1)
    img = cv2.circle(img,(int(width/2),int(height/2)),r3,(255,255,255),1)
    img = cv2.circle(img,(int(width/2),int(height/2)),r4,(255,255,255),1)
    img = cv2.circle(img,(int(width/2),int(height/2)),r5,(255,255,255),1)
    img = cv2.circle(img,(int(width/2),int(height/2)),r6,(255,255,255),1)
    img = cv2.circle(img,(int(width/2),int(height/2)),r7,(255,255,255),1)
    img = cv2.circle(img,(int(width/2),int(height/2)),r8,(255,255,255),1)

def draw_center(img,location,color=(255,255,255),size=5):
    cv2.line(img,location,location,color,size)

def dist(x,y):
    return distance.euclidean(x,y)

def fixParallex():
    global found_dist
    if found_dist <r1:
        found_dist = found_dist - (found_dist*0)
    elif found_dist > r1 and found_dist <r2:
        found_dist = found_dist - (found_dist*0)
    elif found_dist > r2 and found_dist <r3:
        found_dist = found_dist - (found_dist*0)
    elif found_dist > r3 and found_dist <r4:
        found_dist = found_dist - (found_dist*0)
    elif found_dist > r4 and found_dist <r5:
        found_dist = found_dist - (found_dist*0.02)
    elif found_dist > r5 and found_dist <r6:
        found_dist = found_dist - (found_dist*0.05)
    elif found_dist > r6 and found_dist <r7:
        found_dist = found_dist - (found_dist*0.1)
    elif found_dist > r7 and found_dist <r8:
        found_dist = found_dist - (found_dist*0.1)
    else:
        found_dist = found_dist - (found_dist*0.18)

##main code*****************************************************

time.sleep(1)
player1score = []
player2score = []
root = Tk()
root.title('Score Board')
root.geometry('550x100+10+10')
win = Frame(root)
win.pack()
lbl = Label(win,text = " ",font = ('times',50,'bold'), bg = 'black',fg='red', width = 550, height = 100)
lbl.pack(expand= YES, fill = BOTH)
# en = Entry(win, bg = "white")
# en.pack()
def start():
    global found_dist,l1score,l2score,l3score,check,width,height,score,lbl, player, player1score, player2score
    def result():
        root = Tk()
        root.geometry("400x400")
        Label(root, text = f"Score of Player 1: -{sum(player1score)}").pack()
        Label(root, text = f"Score of Player 2: -{sum(player2score)}").pack()
        if sum(player1score)-sum(player2score)>0:
            win = "Player 1"
            Label(root, text = f"{win} won the match").pack()
        elif sum(player1score)-sum(player2score)<0:
            win = "Player 2"
            Label(root, text = f"{win} won the match").pack()
        elif sum(player1score)-sum(player2score) == 0:
            Label(root, text = f"It's a tie").pack()
        else:
            Label(root, text = f"Restart the Match").pack() 
    _, frame = cap.read()
    img = imgmask(frame,thre = threshold)
    try:
        point1,count1,center1 = npsearch(img[:,:,2],red_low,red_high)
        draw_center(img,location = (center1[1],center1[0]),color =(255,255,255),size = 5 )
        print("Arrow detected")
        found_dist = dist(center1,(height/2,width/2))
        #print("Distance : ", found_dist)
        fixParallex()
        #print("Distance : ", found_dist)
        if found_dist <r1:
            score.append(100)
        elif found_dist > r1 and found_dist <r2:
            score.append(80)
        elif found_dist > r2 and found_dist <r3:
            score.append(60)
        elif found_dist > r3 and found_dist <r4:
            score.append(50)
        elif found_dist > r4 and found_dist <r5:
            score.append(40)
        elif found_dist > r5 and found_dist <r6:
            score.append(30)
        elif found_dist > r6 and found_dist <r7:
            score.append(20)
        elif found_dist > r7 and found_dist <r8:
            score.append(10)
        else:
            score.append(0)

        l3score = l2score
        l2score = l1score
        l1score = score[-1]

        if(l3score == l2score == l1score):
            
            if(check == 2):
                time = str(datetime.datetime.now())[:-7]
                fl = open("record.csv","a")
                fl.write(f"{player},{time},{l3score}\n")
                fl.close()
                if player == "Player 1":
                    player1score.append(l3score)
                else:
                    player2score.append(l3score)
                print('Score : ', l3score)
                lbl.config(text="Score : "+str(l3score))
                check = 0
        else:
            
            if(check == 1):
                print('Calculating Score')
                lbl.config(text="Calculating Score")
                check = 2
            
    except Exception as e:
        if ('many' in str(e)):
            print('No Arrow detected :')
            lbl.config(text="No Arrow Detected")
            check = 1
        else:
            print('Error : ', e)
        print(e)
    draw_circle(frame)
    draw_center(frame,location = (int(width/2),int(height/2)),color =(255,255,255),size = 5)
    ##print(img[:,:,2])
    ##print(img)
    
    cv2.imshow('Original Image',frame)
    cv2.imshow('Processed Image',img)
    k = cv2.waitKey(20)
    
    if k == ord("s"):
        if player == "Player 1":
            player = "Player 2"
        else:
            player = "Player 1"
    if k == ord("r"):
        result()
    if k==27:
        cap.release()
        cv2.destroyAllWindows()
    else:
        root.after(1,start)
        

start()
root.mainloop()

