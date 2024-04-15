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
os.chdir("/Users/markus/Documents/Clicker heroes stuff")

for hero in Guilded_heroes[1:Guilded_heroes.index(MAX_HERO)+1][::-1]:
    print(hero)


