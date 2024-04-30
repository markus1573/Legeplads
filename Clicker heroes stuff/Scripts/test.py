import pyautogui as ag
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from Functions import *
import time
import glob
from Hero_info import *
from Skill_info import *
if sys.platform == "win32":
    os.chdir("C:/Users/marku/Documents/GitHub/Legeplads/Clicker heroes stuff")
elif sys.platform == "darwin":
    os.chdir("/Users/markus/Documents/Legeplads/Clicker heroes stuff")


# # im = cv2.imread("Photos/Temp/old/1Get_Lvl.png")
# im = cv2.imread("Photos/Logged_Screenshots/Get_Lvl.png")

# im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
# im_resized = cv2.resize(im_gray, (0,0), fx = 4, fy = 4, interpolation = cv2.INTER_LINEAR)
# im_blurred = cv2.medianBlur(im_resized, 3)
# im_thresh = (im_blurred < 230).astype(np.uint8)*255
# im_eroded = cv2.erode(im_thresh, np.ones((2,2),np.uint8), iterations = 1)
# im_dilated = cv2.dilate(im_eroded, np.ones((2,2),np.uint8), iterations = 1)
# im_blurred = cv2.medianBlur(im_dilated, 3)
# config = r"--psm 13, outputbase digits"
# text = pytesseract.image_to_string(im_blurred,config=config)
# text_int = extract_numeric(text)
# if text == "" or text_int == "":
#     lvl = 0
#     print(f"lvl: {lvl}")
    
#     cv2.imwrite("Photos/Temp/1Get_Lvl.png",im)
#     cv2.imwrite("Photos/temp/2Get_Lvl_gray.png",im_gray)
#     cv2.imwrite("Photos/temp/3Get_Lvl_resized.png",im_resized)
#     cv2.imwrite("Photos/temp/4Get_Lvl_thresh.png",im_thresh)
#     cv2.imwrite("Photos/temp/5Get_Lvl_eroded.png",im_eroded)
#     cv2.imwrite("Photos/temp/6Get_Lvl_dilated.png",im_dilated)
#     cv2.imwrite("Photos/temp/7Get_Lvl_blurred.png",im_blurred)
# else:
#     lvl = text_int
#     print(f"lvl: {lvl}")
    
#     cv2.imwrite("Photos/Temp/1Get_Lvl.png",im)
#     cv2.imwrite("Photos/temp/2Get_Lvl_gray.png",im_gray)
#     cv2.imwrite("Photos/temp/3Get_Lvl_resized.png",im_resized)
#     cv2.imwrite("Photos/temp/4Get_Lvl_thresh.png",im_thresh)
#     cv2.imwrite("Photos/temp/5Get_Lvl_eroded.png",im_eroded)
#     cv2.imwrite("Photos/temp/6Get_Lvl_dilated.png",im_dilated)
#     cv2.imwrite("Photos/temp/7Get_Lvl_blurred.png",im_blurred)


image = cv2.imread("Photos/Tmp/old/Get_Zone.png")
im_resized = cv2.resize(image, (0,0), fx = 4, fy = 4, interpolation = cv2.INTER_LINEAR)
im_blurred = cv2.medianBlur(im_resized, 3)
target_color = (56, 158, 241)
mask = cv2.inRange(im_blurred, target_color, target_color)
im_thresh = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY_INV)[1]
im_eroded = cv2.erode(im_thresh, np.ones((2,2),np.uint8), iterations = 2)
im_dilated = cv2.dilate(im_eroded, np.ones((2,2),np.uint8), iterations = 1)
im_blurred = cv2.medianBlur(im_dilated, 3)
text = pytesseract.image_to_string(im_blurred,config="--psm 4, outputbase digits")
if text == "":
    pass
else:
    zone_lvl = extract_numeric(text)
    # cv2.imwrite("Photos/Logged_Screenshots/Get_Zone.png",image)
    cv2.imwrite("Photos/Tmp/1Get_Zone.png",image)
    cv2.imwrite("Photos/Tmp/2Get_Zone_resized.png",im_resized)
    cv2.imwrite("Photos/Tmp/3Get_Zone_thresh.png",im_thresh)
    cv2.imwrite("Photos/Tmp/4Get_Zone_eroded.png",im_eroded)
    cv2.imwrite("Photos/Tmp/5Get_Zone_dilated.png",im_dilated)
    cv2.imwrite("Photos/Tmp/6Get_Zone_blurred.png",im_blurred)    
    
    print(zone_lvl)


