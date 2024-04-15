import os
from Functions import *
import pyautogui as ag
import numpy as np
import cv2
import pygetwindow as gw

offsetx = 207
offsety = 210

files = range(14,15)
for i in files:
    target_color = (41, 92, 212)
    tolerance = 5

    screenshot_crop = cv2.imread("Photos/Screenshots/Screenshot"+str(i)+".png")
    screenshot_crop_copy = screenshot_crop.copy() # For showing with circles
    screenshot_crop_copy2 = screenshot_crop.copy() # For showing with circles
    screenshot_crop = Remove_buttons(screenshot_crop)

    # Search for the target color in the screenshot
    matches = search_pixel_color(screenshot_crop, target_color, tolerance)

    print(f"Found {str(len(matches))} matches in screenshot{str(i)}")
    # Create small circle around the matches
    if not matches:
        print("No matches found")
        pass
    if len(matches) > 40:
        for match in matches:
            cv2.circle(screenshot_crop_copy, match, 10, (0, 255, 0), -1)
        cv2.imshow("Screenshot"+str(i), screenshot_crop_copy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # calculate the median position of detected matches
        median_x = int(np.median([match[0] for match in matches]))
        median_y = int(np.median([match[1] for match in matches]))
        if ag.pyscreeze.is_retina:
            final_match = ((median_x), (median_y))
        
        cv2.circle(screenshot_crop_copy2, final_match, 10, (0, 255, 0), -1)
        cv2.imshow("Screenshot"+str(i), screenshot_crop_copy2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    else:
        None