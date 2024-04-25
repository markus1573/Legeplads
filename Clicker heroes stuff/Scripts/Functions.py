import pyautogui as ag
import numpy as np
import cv2
import pytesseract
import threading
import torch
import re
import time
from Hero_info import *
from Skill_info import *
import os
import glob
import sys
from RUN import GUILDED_HERO, DEEP_RUN, START_IDLE, MAX_HERO
from pynput.keyboard import Listener, KeyCode, Key, HotKey

# offsetx = 207
# offsety = 210


ASCENDING = False
EARLY_HEROES_BOUGHT = False

def FocusWindowAndGetWindowPOS():
    """
    
    """    
    
    window = ag.locateCenterOnScreen("Photos/Buttons/FocusWindow_button.png",confidence=0.75)
    if window == None:
        print("Could not find window")
        raise ValueError("Could not find window")
    else:
        ag.doubleClick(window,_pause=False)
        ag.sleep(0.1)
    
    WrenchOffset = (44,-25)

    # Get window placement
    global window_width, window_height
    # if ag.pyscreeze.is_retina():
    #     window_width = int(1256*2)
    #     window_height = int(696.5*2)
    # else:
    window_width = int(1256)
    window_height = int(696.5)
    # Locate center of window
    Wrench = ag.locateCenterOnScreen("Photos/Buttons/wrench_button.png",confidence=0.75)
    if Wrench == None:
        raise ValueError("Could not find wrench button")
    
    # Get window corners
    TopRightCorner = (Wrench[0] + WrenchOffset[0], Wrench[1] + WrenchOffset[1])
    TopleftCorner = (TopRightCorner[0] - window_width, TopRightCorner[1])
    BottomRightCorner = (TopRightCorner[0], TopRightCorner[1] + window_height)
    BottomLeftCorner = (BottomRightCorner[0] - window_width, BottomRightCorner[1])

    # move mouse to wrench and all corners of the window
    # ag.moveTo(Wrench,_pause=False)
    # ag.sleep(1)
    # ag.moveTo(TopRightCorner,_pause=False)
    # ag.sleep(1)
    # ag.moveTo(TopleftCorner,_pause=False)
    # ag.sleep(1)
    # ag.moveTo(BottomLeftCorner,_pause=False)
    # ag.sleep(1)
    # ag.moveTo(BottomRightCorner,_pause=False)
    # ag.sleep(1)

    # Get window region
    global bbox
    if ag.pyscreeze.is_retina():
        bbox = (TopleftCorner[0]*2, TopleftCorner[1]*2, window_width*2, window_height*2)
    else:
        bbox = TopleftCorner + (window_width, window_height)

    global offsetx, offsety
    offsetx, offsety = TopleftCorner
    offsetx = int(offsetx)
    offsety = int(offsety)
    return bbox, offsetx, offsety




# def check_pixel_color(pixel_color, target_color, tolerance):
#     """
#     Check if a pixel color matches the target color within the specified tolerance.
    
#     Parameters
#     ----------
#     pixel_color : tuple
#         The color of the pixel.
#     target_color : tuple
#         The target color of the pixel.
#     tolerance : int
#         The color tolerance of the pixel.

#     Returns
#     -------
#     bool
#         True if the pixel color matches the target color within the specified tolerance, False otherwise.
#     """
#     if isinstance(pixel_color, int) or isinstance(pixel_color, np.uint8):
#         pixel_color = (pixel_color, pixel_color, pixel_color)
#     if isinstance(target_color, int) or isinstance(target_color, np.uint8):
#         target_color = (target_color, target_color, target_color)        

#     elif len(pixel_color) != len(target_color):
#         raise ValueError("Pixel and target color must have the same number of channels")
    
#     for i in range(3):  # Check RGB channels
#         if abs(pixel_color[i] - target_color[i]) > tolerance:
#             return False
#     return True


# def search_pixel_color(image, target_color:tuple, tolerance: int):
#     """
#     Search for the target color in the image within the specified tolerance.

#     Parameters
#     ----------
#     image : array
#         The cropped screenshot.
#     target_color : tuple
#         The target color of the pixel.
#     tolerance : int
#         The color tolerance of the pixel.

#     Returns
#     -------
#     matches : list
#         A list of tuples containing the coordinates of the matches.
#     """
#     if len(image.shape) != 3:
#         h,w = image.shape
#     else:
#         h, w, _ = image.shape
#     matches = []

#     for y in range(h):
#         for x in range(w):
#             if check_pixel_color(image[y, x], target_color, tolerance):
#                 matches.append((x, y))

#     return matches


# def Remove_buttons(image):
#     """
#     TODO: Mangler at få dette til at virke til alle skærmstørrelser.

#     Remove the ritual button, the farmmode button and the mute button from the screenshot.

#     Parameters
#     ----------
#     image : array
#         The screenshot.

#     Returns
#     -------
#     image : array
#         The cropped screenshot with the buttons removed.
#     """
   
    
#     # location of ritual button:
#     ritual_region = Region([628,450,48,48])

#     # remove ritual button from screenshot
#     image[ritual_region[1]:ritual_region[1]+ritual_region[3],
#           ritual_region[0]:ritual_region[0]+ritual_region[2],:] \
#             [image[ritual_region[1]:ritual_region[1]+ritual_region[3],
#           ritual_region[0]:ritual_region[0]+ritual_region[2],:][:,:,2]>200] = [0,0,0]

#     # Location of farmmode button:
#     farmmode_region = Region([1193,182,38,38])

#     # remove farmmode button from screenshot
#     image[farmmode_region[1]:farmmode_region[1]+farmmode_region[3],
#           farmmode_region[0]:farmmode_region[0]+farmmode_region[2],:] \
#             [image[farmmode_region[1]:farmmode_region[1]+farmmode_region[3],
#           farmmode_region[0]:farmmode_region[0]+farmmode_region[2],:][:,:,2]==214] = [0,0,0]

#     #location of mute button:
#     mute_region = Region([1193,625,38,38])

#     # remove mute button from screenshot
#     image[mute_region[1]:mute_region[1]+mute_region[3],
#           mute_region[0]:mute_region[0]+mute_region[2],:] \
#             [image[mute_region[1]:mute_region[1]+mute_region[3],
#           mute_region[0]:mute_region[0]+mute_region[2],:][:,:,2]==210] = [0,0,0]
#     return image


def Region(region:tuple|list):
    """
    """
    if ag.pyscreeze.is_retina():
        return ((region[0]+offsetx)*2,(region[1]+offsety)*2,region[2]*2,region[3]*2)
    else:
        return (region[0]+offsetx,region[1]+offsety,region[2],region[3])


def Screenshot(region=None):
    """
    Take a screenshot of the game window.

    Parameters
    ----------
    crop : bool, optional
        Crop the screenshot to the game window. The default is True.

    Returns
    -------
    screenshot_crop : array
        The cropped screenshot.
    """
    screenshot = ag.pyscreeze._load_cv2(ag.screenshot(), grayscale=False)
    if region:
        screenshot = screenshot[region[1]:region[1]+region[3], region[0]:region[0]+region[2]]         
    return screenshot


def Find_fish_new():
    screenshot_cropped = Screenshot(region=bbox)
    screenshot_cropped = cv2.cvtColor(screenshot_cropped, cv2.COLOR_BGR2RGB)
    results = model(screenshot_cropped)
    if results.xyxy[0].shape[0] > 0:
        x1, y1, x2, y2, _, _ = results.xyxy[0].numpy()[0]
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        if ag.pyscreeze.is_retina():
            return (x//2+offsetx, y//2+offsety)
        else:
            return (x+offsetx,y+offsety)
    else:
        return None


# def Find_fish(target_color=(41, 92, 212), tolerance=5):
#     """
#     Search for fish in the game window and place mouse on it.
    
#     Parameters
#     ----------
#     target_color : tuple. Default: (41,92,212)

#     tolerance : int. Default: 5

#     Returns
#     -------
#     tuple
#         A tuple containing the coordinates of the fish.
#     """
#     # Get the screenshot
#     screenshot_crop = Screenshot(region=bbox)
#     cv2.imwrite("Photos/Logged_Screenshots/Screenshot1.png",screenshot_crop)

#     # Remove ritual button from screenshot
#     screenshot_crop = Remove_buttons(screenshot_crop)
#     cv2.imwrite("Photos/Logged_Screenshots/Screenshot2.png",screenshot_crop)
    
#     # Search for the target color in the screenshot
#     matches = search_pixel_color(screenshot_crop, target_color, tolerance)
#     # print(f"Found {str(len(matches))} matches")
#     if len(matches) > 40:
#         # Calculate the average position of detected matches
#         avg_x = int(np.mean([match[0] for match in matches]))
#         avg_y = int(np.mean([match[1] for match in matches]))

#         # calculate the median position of detected matches
#         median_x = int(np.median([match[0] for match in matches]))
#         median_y = int(np.median([match[1] for match in matches]))

#         if ag.pyscreeze.is_retina:
#             return (median_x//2+offsetx, median_y//2+offsety)
#         else:
#             return (median_x+offsetx,median_y+offsety)
#     else:
#         return None


def BuyAllUpgrades():
    Scroll_Bottom()
    region = Region((338,620,185,50))
    upgrades_button = ag.locateCenterOnScreen("Photos/Buttons/BuyAllUpgrades_button.png",region=region,confidence=0.75)
    if upgrades_button:
        ag.click(upgrades_button,_pause=False)
        ag.sleep(0.1)
    return


def Scroll_Bottom():
    Stop_background_processes()
    ag.moveTo(575+offsetx,668+offsety,_pause=False)
    ag.dragTo(575+offsetx,670+offsety,duration=0.2,_pause=False)
    ag.sleep(0.1)
    Start_background_processes()
    return


def Scroll_Top():
    Stop_background_processes()
    ag.moveTo(575+offsetx,268+offsety,_pause=False)
    ag.dragTo(575+offsetx,265+offsety,duration=0.2,_pause=False)
    ag.sleep(0.1)
    Start_background_processes()
    return


def Scroll_Up_fast(times=1):
    Stop_background_processes()
    for _ in range(times):
        ag.click(575+offsetx,250+offsety,clicks=21,interval=0.025,_pause=False)
    ag.sleep(0.1)
    Start_background_processes()
    return


def Scroll_Down_fast(times=1):
    Stop_background_processes()
    for _ in range(times):
        ag.click(575+offsetx,685+offsety,clicks=21,interval=0.025,_pause=False)
    ag.sleep(0.1)
    Start_background_processes()
    return


def Hero_imsearch(hero:str):
    region = Region([343,240,125,385])
    region_buyallupgrades = Region([338,620,185,50])
    scrolled_up = False
    if not standard_run_thread.program_running:
        return
    if GUILDED_HERO !=None and (GUILDED_HERO == hero or hero in GUILDED_HERO_COPIES):
        while True:
            box = ag.locateOnScreen(f"Photos/Heroes/Guilded/{hero}_guilded.png",region=region,confidence=0.75)
            if box == None:
                if not standard_run_thread.program_running:
                    return
                buy_all_upgrades = ag.locateCenterOnScreen("Photos/Buttons/BuyAllUpgrades_button.png",region=region_buyallupgrades,confidence=0.75)
                if buy_all_upgrades == None:
                    if scrolled_up == True:
                        Scroll_Top()
                        scrolled_up = False
                    else:
                        Scroll_Down_fast(1)
                else:
                        ag.click(buy_all_upgrades,_pause=False)
                        ag.sleep(0.1)
                        Scroll_Up_fast()
                        scrolled_up = True
            else:
                loc_heroname = ((box[0]+box[2]),box[1]+box[3]//2)
                loc_buyhero = (loc_heroname[0]-335,loc_heroname[1]+30)
                return loc_buyhero
    else:
        while True:
            box = ag.locateOnScreen(f"Photos/Heroes/Normal/{hero}.png",region=region,confidence=0.75)
            if box == None:
                if not standard_run_thread.program_running:
                    return
                buy_all_upgrades = ag.locateCenterOnScreen("Photos/Buttons/BuyAllUpgrades_button.png",region=region_buyallupgrades,confidence=0.75)
                if buy_all_upgrades == None:
                    if scrolled_up == True:
                        Scroll_Top()
                        scrolled_up = False
                    else:
                        Scroll_Down_fast(1)
                else:
                        ag.click(buy_all_upgrades,_pause=False)
                        ag.sleep(0.1)
                        Scroll_Up_fast()
                        scrolled_up = True
            else:
                loc_heroname = ((box[0]+box[2]),box[1]+box[3]//2)
                loc_buyhero = (loc_heroname[0]-335,loc_heroname[1]+30)
                return loc_buyhero


def Lvl_Hero_To(heroes:str | list[str],Lvl=None,pprint:bool=True):
    if isinstance(heroes,str):
        heroes = [heroes]
    for hero in heroes:
        first_time_on_hero = False
        if not ASCENDING and not standard_run_thread.running:
            break
        if Lvl != None:
            lvl = Lvl
        else:
            lvl = Hero_Info[hero][2]
        counter = 0
        zero_counter = 0
        lvled_to_x000 = 0
        if GUILDED_HERO != None:
            # if hero == Guilded_heroes[Guilded_heroes.index(GUILDED_HERO)+1]:
            if hero in Guilded_heroes and Guilded_heroes.index(hero) > Guilded_heroes.index(GUILDED_HERO):
                guild_hero(hero)
        if pprint:
            print(f"Leveling {hero} to {str(lvl)}")
        loc = Hero_imsearch(hero)
        init_value = Get_Lvl(loc)
        while ASCENDING or standard_run_thread.running:
            if init_value == 0:
                first_time_on_hero = True
                zero_counter += 1
                if zero_counter == 4:
                    Stop_autoclicker()
                    loc = Hero_imsearch(hero)
                    zero_counter = 0
            if init_value >= lvl:
                if pprint:
                    print(f"{hero} leveled to {str(init_value)}. Moving on.")
                break
            if hero in Tsuchi_Madzi and init_value > 1000 and lvled_to_x000 <= 1000:
                print(f"{hero} is 1000. Buying all upgrades.")
                lvled_to_x000 = 1001
                BuyAllUpgrades()
                loc = Hero_imsearch(hero)
            elif hero in Tsuchi_Madzi and init_value > 2000 and lvled_to_x000 <= 2000:
                print(f"{hero} is 2000. Buying all upgrades.")
                lvled_to_x000 = 2001
                BuyAllUpgrades()
                loc = Hero_imsearch(hero)
            elif hero in Tsuchi_Madzi and init_value > 4000 and lvled_to_x000 <= 4000:
                print(f"{hero} is 4000. Buying all upgrades.")
                lvled_to_x000 = 4001
                BuyAllUpgrades()
                loc = Hero_imsearch(hero)
            elif hero in Tsuchi_Madzi and init_value > 8000 and lvled_to_x000 <= 8000:
                print(f"{hero} is 8000. Buying all upgrades.")
                lvled_to_x000 = 8001
                BuyAllUpgrades()
                loc = Hero_imsearch(hero)
            ag.keyDown("q",_pause=False)
            ag.sleep(0.1)
            ag.click(loc,_pause=False)
            ag.keyUp("q",_pause=False)
            init_value = Get_Lvl(loc)
            if init_value >= lvl:
                if pprint:
                    print(f"{hero} leveled to {str(init_value)}. Moving on.")
                break
            if init_value > 150 and counter < 5:
                if first_time_on_hero:
                    BuyAllUpgrades()
                    loc = Hero_imsearch(hero)
                counter = 5
            if not IDLE:
                Start_autoclicker()
            else:
                ag.moveTo(loc[0]-100,loc[1],_pause=False)
            ag.sleep(5)
            counter += 1
            if counter == 4:
                if pprint:
                    print(f"Tried to level {hero} to {str(lvl)} 4 times. Buying all upgrades.")
                Stop_autoclicker()
                BuyAllUpgrades()
                loc = Hero_imsearch(hero)
                counter = 0
            Stop_autoclicker()
        ag.sleep(0.1)
    return
            

def extract_numeric(text):
    numeric_text = re.sub(r'[^0-9]', '', text)
    if numeric_text == '':
        return numeric_text
    return int(numeric_text)

    
def Get_Lvl(hero_loc):
    loc = (hero_loc[0]+215,hero_loc[1]-20)
    if ag.pyscreeze.is_retina():
        bbox = (loc[0]*2,loc[1]*2,245,45)
    else:
        bbox = (hero_loc[0]+215,hero_loc[1]-20,128,28)
    im = Screenshot(region=bbox)
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im_thresh = (im_gray < 255).astype(np.uint8)*255
    im_resized = cv2.resize(im_thresh, (0,0),fx = 4, fy = 4, interpolation = cv2.INTER_CUBIC)
    im_eroded = cv2.erode(im_resized, np.ones((2,2),np.uint8), iterations = 2)
    text = pytesseract.image_to_string(im_eroded,config="--psm 13, outputbase digits")
    text_int = extract_numeric(text)
    if text == "" or text_int == "":
        lvl = 0
        # print(f"lvl: {lvl}")
        ag.click(loc[0]+75,loc[1]+15,_pause=False)
        ag.sleep(0.1)
        # cv2.imwrite("Photos/Logged_Screenshots/Get_Lvl.png",im)
        return lvl
    else:
        lvl = text_int
        # print(f"lvl: {lvl}")
        # cv2.imwrite("Photos/Logged_Screenshots/Get_Lvl.png",im)
        return lvl


def BuyEarlyHeroes():
    heroes = All_Heroes[:26]
    print("Buying early heroes")
    for i in range(1,4):
        if standard_run_thread.running:
            Lvl_Hero_To(heroes,Lvl=50*i,pprint=False)
            BuyAllUpgrades()
    get_skill_timers()
    if Infinite_skills["Golden Clicks"]:
        Go_active()
        Start_use_skills()


def BuyHero(heroes):
    if isinstance(heroes,str):
        heroes = [heroes]
    for hero in heroes:
        loc = Hero_imsearch(hero)
        if loc == None:
            break
        ag.keyDown("q",_pause=False)
        ag.sleep(0.1)
        ag.click(loc,_pause=False)
        ag.keyUp("q",_pause=False)
    return


def ClickMonster(clicks=1):
    loc = (950+offsetx,350+offsety)
    ag.click(loc,clicks=clicks,interval=0.008,_pause=False)
    ag.sleep(0.1)
    return


def Go_idle():
    global IDLE
    IDLE = True
    Stop_autoclicker()
    region = Region([1176,350,55,55])
    loc = ag.locateCenterOnScreen("Photos/Buttons/Autoclicker_button.png",region=region,confidence=0.75)
    if loc:
        ag.keyDown("c",_pause=False)
        ag.sleep(0.1)
        ag.click(loc,_pause=False)
        ag.keyUp("c",_pause=False)
        ag.sleep(0.1)
    return


def Go_active():
    global IDLE
    IDLE = False
    ag.keyDown("c",_pause=False)
    ag.sleep(0.1)
    ClickMonster(10)
    ag.keyUp("c",_pause=False)
    ag.sleep(0.1)
    return


def Get_Zone():
    region = Region([912,20,48,50])
    image = Screenshot(region=region)
    target_color = (56, 158, 241)
    mask = cv2.inRange(image, target_color, target_color)
    thresholded = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY_INV)[1]
    resized = cv2.resize(thresholded, (0,0),fx = 4, fy = 4, interpolation = cv2.INTER_CUBIC)
    eroded = cv2.erode(resized, np.ones((2,2), np.uint8), iterations = 2)
    text = pytesseract.image_to_string(eroded,config=f"--psm 6, outputbase digits")
    if text == "":
        return Get_Zone()
    else:
        zone_lvl = extract_numeric(text)
        return zone_lvl

def Has_duplicates(hero):
    hero = re.sub(r'[0-9]+', '', hero)
    duplicates = glob.glob("Photos/Heroes/Normal/"+hero+"*.png")
    if len(duplicates) > 1:
        duplicates = [duplicates[i].split("/")[-1] for i in range(len(duplicates))]
        duplicates = [duplicates[i].split(".")[0] for i in range(len(duplicates))]
        return duplicates
    else:
        return None


def Guild_scroll():
    ag.click(1103+offsetx,485+offsety,_pause=False,clicks=19,interval=0.05)
    ag.sleep(0.1)


def guild_hero(hero:str):
    Stop_background_processes()
    Stop_check_ascend()
    region = Region([70,365,100,325])
    print(region)
    Scroll_Bottom()
    guild_button_loc = ag.locateCenterOnScreen("Photos/Buttons/Guilded_button.png",region=region,confidence=0.75)
    ag.click(guild_button_loc,_pause=False)
    ag.sleep(0.1)
    guild_hero_loc = Guild_imsearch(hero)
    ag.sleep(0.1)
    ag.keyDown("q",_pause=False)
    ag.sleep(0.1)
    ag.click(guild_hero_loc,_pause=False)
    ag.sleep(0.1)
    ag.keyUp("q",_pause=False)
    ag.sleep(0.1)
    check_guild_region = Region([135,115,950,390])
    loc = ag.locateCenterOnScreen(f"Photos/Guilds/Guilded/{hero}_guilded.png",region=check_guild_region,confidence=0.75)
    ag.sleep(0.1)
    if loc == None:
        print(f"Could not guild {hero}. Not enough HS.")
    else:
        global GUILDED_HERO
        GUILDED_HERO = hero
        global GUILDED_HERO_COPIES
        duplicates = Has_duplicates(hero)
        if duplicates:
            GUILDED_HERO_COPIES = duplicates
        else:
            GUILDED_HERO_COPIES = []
    exit_loc = ag.locateCenterOnScreen("Photos/Buttons/Exit_button.png",confidence=0.75)
    ag.click(exit_loc,_pause=False)
    ag.sleep(0.1)
    Start_background_processes()
    Start_check_ascend()


def Guild_imsearch(hero:str,counter=0):
    region = Region([135,115,950,390])
    if counter == 3:
        raise ValueError("Could not find hero")
    if GUILDED_HERO == hero:
        loc = ag.locateCenterOnScreen(f"Photos/Guilds/Guilded/{hero}_guilded.png",region=region,confidence=0.75)
        if loc == None:
            Guild_scroll()
            return Guild_imsearch(hero,counter=counter+1)
        return loc
    else:
        loc = ag.locateCenterOnScreen(f"Photos/Guilds/Normal/{hero}.png",region=region,confidence=0.75)
        if loc == None:
            Guild_scroll()
            return Guild_imsearch(hero,counter=counter+1)
        return loc
   

def skill_locs_and_regions():
    clickstorm_loc = 650+offsetx,190+offsety
    powersurge_loc = 650+offsetx,245+offsety
    lucky_strike_loc = 650+offsetx,300+offsety
    metal_detector_loc = 650+offsetx,355+offsety
    golden_clicks_loc = 650+offsetx,410+offsety
    super_clicks_loc = 650+offsetx,520+offsety
    energize_loc = 650+offsetx,575+offsety
    reload_loc = 650+offsetx,630+offsety

    clickstorm_region = Region([705,245,150,35])
    powersurge_region = Region([705,285,150,35])
    lucky_strike_region = Region([705,340,150,35])
    metal_detector_region = Region([705,395,150,35])
    golden_clicks_region = Region([705,450,150,50])
    super_clicks_region = Region([705,565,150,35])
    energize_region = Region([705,605,150,35])
    reload_region = Region([705,605,150,35])

    global skill_locs, skill_regions
    skill_locs = dict(zip(All_skills, 
    [clickstorm_loc, powersurge_loc,lucky_strike_loc,
        metal_detector_loc,golden_clicks_loc,
        super_clicks_loc,energize_loc,reload_loc]))

    skill_regions = dict(zip(All_skills,
    [clickstorm_region, powersurge_region,
        lucky_strike_region, metal_detector_region, 
        golden_clicks_region, super_clicks_region, 
        energize_region, reload_region]))
    
    return skill_locs,skill_regions


def get_skill_timers():
    Stop_background_processes()
    Stop_check_ascend()
    skill_locs,skill_regions = skill_locs_and_regions()
    global skill_durations, skill_cooldowns,skill_durations_copy, skill_cooldowns_copy
    skill_durations = {}
    skill_cooldowns = {}
    skill_durations_copy = {}
    skill_cooldowns_copy = {}
    for skill in All_skills:
        if standard_run_thread.running:
            global duration, cooldown
            ag.moveTo(skill_locs[skill],_pause=False)
            ag.sleep(0.2)
            image = Screenshot(region=skill_regions[skill])
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # cv2.imwrite(f"Photos/Logged_Screenshots/Skills/{skill}.png",gray)
            resized = cv2.resize(gray, (0,0),fx = 4, fy = 4, interpolation = cv2.INTER_CUBIC)
            text = pytesseract.image_to_string(resized,config="--psm 6")
            # pattern = r'(?:Duration|Cooldown):\s*(\d{1,2}m\s*)?(\d+\.\d{2}s|\d{1,2}s)?'
            pattern = r'(?:Duration|Cooldown):\s*(\d{1,2}h\s*)?(\d{1,2}m\s*)?(\d+\.\d{2}s|\d{1,2}s)?'
            matches = re.findall(pattern, text)
            if len(matches) == 3:
                duration = [match.replace(" ","").replace("h","").replace("m","").replace("s","") for match in matches[0]]
                duration = [int(float(i)) if i !="" else 0 for i in duration]
                duration = duration[0]*3600 + duration[1]*60 + duration[2]
                cooldown = [match.replace(" ","").replace("h","").replace("m","").replace("s","") for match in matches[1]]
                cooldown = [int(float(i)) if i !="" else 0 for i in cooldown]
                cooldown = cooldown[0]*3600 + cooldown[1]*60 + cooldown[2]
            elif len(matches) == 2:
                duration = [match.replace(" ","").replace("h","").replace("m","").replace("s","") for match in matches[0]]
                duration = [int(float(i)) if i !="" else 0 for i in duration]
                duration = duration[0]*3600 + duration[1]*60 + duration[2]
                cooldown = [match.replace(" ","").replace("h","").replace("m","").replace("s","") for match in matches[1]]
                cooldown = [int(float(i)) if i !="" else 0 for i in cooldown]
                cooldown = cooldown[0]*3600 + cooldown[1]*60 + cooldown[2]
            elif len(matches) == 1:
                duration = None
                cooldown = [match.replace(" ","").replace("h","").replace("m","").replace("s","") for match in matches[0]]
                cooldown = [int(float(i)) if i !="" else 0 for i in cooldown]
                cooldown = cooldown[0]*3600 + cooldown[1]*60 + cooldown[2]
            skill_durations[skill] = duration
            skill_cooldowns[skill] = cooldown
            ag.sleep(0.1)
    for skill in Main_skills:
        if skill_durations[skill] >= skill_cooldowns[skill]:
            global Infinite_skills
            Infinite_skills[skill] = True
    Start_background_processes()
    Start_check_ascend()
    global EARLY_HEROES_BOUGHT
    EARLY_HEROES_BOUGHT = True
    return 


def Get_new_guilds(first_run=True):
    if GUILDED_HERO != None:
        new_guild_region = Region([1165,550,50,50])
        window_region = Region([300,120,675,430])
        new_guild_loc = ag.locateCenterOnScreen("Photos/Buttons/New_guild_button.png",region=new_guild_region,confidence=0.75)
        if new_guild_loc != None:
            ag.click(new_guild_loc,_pause=False)
            ag.sleep(0.1)
            ag.click(window_width/2+offsetx,window_height/2+offsety,_pause=False)
            ag.sleep(2)
            open_all_guilds_loc = ag.locateCenterOnScreen("Photos/Buttons/Open_all_guilds_button.png",region=window_region,confidence=0.75)
            if open_all_guilds_loc == None:
                exit_loc = ag.locateCenterOnScreen("Photos/Buttons/Exit_button.png",confidence=0.75)
                ag.click(exit_loc,_pause=False)
                ag.sleep(0.1)
                return Get_new_guilds(first_run=False)
            else:
                ag.click(open_all_guilds_loc,_pause=False)
                ag.sleep(0.1)
                exit_loc = ag.locateCenterOnScreen("Photos/Buttons/Exit_button.png",confidence=0.75)
                ag.click(exit_loc,_pause=False)
                ag.sleep(0.1)
                guild_hero(GUILDED_HERO)
                ag.sleep(0.1)
        elif new_guild_loc == None and not first_run:
            guild_hero(GUILDED_HERO)
            ag.sleep(0.1)


def Use_calculator():
    wrench_region = Region([1195,9,35,35])
    save_region = Region([300,120,675,430])
    wrench_loc = ag.locateCenterOnScreen("Photos/Buttons/Wrench_button.png",region=wrench_region,confidence=0.75)
    ag.click(wrench_loc,_pause=False)
    ag.sleep(0.1)
    save_loc = ag.locateCenterOnScreen("Photos/Buttons/Save_button.png",region=save_region,confidence=0.75)
    ag.click(save_loc,_pause=False)
    ag.sleep(3)
    cancel_loc = ag.locateCenterOnScreen("Photos/Buttons/Cancel_button.png",region=save_region,confidence=0.75)
    if cancel_loc != None:
        ag.click(cancel_loc,_pause=False)
        ag.sleep(3)
    else:
        ag.sleep(3)
        cancel_loc = ag.locateCenterOnScreen("Photos/Buttons/Cancel_button.png",region=save_region,confidence=0.75)
        if cancel_loc != None:
            ag.click(cancel_loc,_pause=False)
            ag.sleep(3)
    calculator_loc = ag.locateCenterOnScreen("Photos/Buttons/Calculator_button.png",confidence=0.75)
    if calculator_loc == None:
        exit_loc = ag.locateCenterOnScreen("Photos/Buttons/Exit_button.png",confidence=0.75)
        ag.click(exit_loc,_pause=False)
        ag.sleep(3)
        return
    ag.click(calculator_loc,_pause=False)
    ag.sleep(3)
    ag.moveRel(0,300,_pause=False)
    ag.sleep(0.1)
    ag.scroll(50,_pause=False)
    ag.sleep(3)
    pastesave_loc = ag.locateCenterOnScreen("Photos/Buttons/Paste_save_button.png",confidence=0.75)
    ag.click(pastesave_loc,_pause=False)
    ag.sleep(3)
    ag.hotkey("command","v",_pause=False,interval=0.1)
    ag.sleep(3)
    calculator_import_loc = ag.locateCenterOnScreen("Photos/Buttons/Calculator_import_button.png",confidence=0.75)
    ag.click(calculator_import_loc,_pause=False)
    ag.sleep(3)
    import_save_loc = ag.locateCenterOnScreen("Photos/Buttons/Import_save_button.png",confidence=0.75)
    ag.click(import_save_loc,_pause=False)
    ag.sleep(3)
    ag.hotkey("command","c",_pause=False,interval=0.1)
    ag.sleep(3)
    clickerheroes_loc = ag.locateCenterOnScreen("Photos/Buttons/Clickerheroes_button.png",confidence=0.75)
    ag.click(clickerheroes_loc,_pause=False)
    ag.sleep(3)
    import_loc = ag.locateCenterOnScreen("Photos/Buttons/Import_button.png",region=save_region,confidence=0.75)
    ag.click(import_loc,_pause=False)
    ag.sleep(3)
    ag.click(_pause=False)
    ag.sleep(3)
    ag.hotkey("command","v",_pause=False,interval=0.1)
    ag.sleep(3)
    okay_loc = ag.locateCenterOnScreen("Photos/Buttons/Okay_button.png",region=save_region,confidence=0.75)
    ag.click(okay_loc,_pause=False)
    ag.sleep(3)
    exit_loc = ag.locateCenterOnScreen("Photos/Buttons/Exit_button.png",confidence=0.75)
    ag.click(exit_loc,_pause=False)
    ag.sleep(3)


def Search_latest_hero(hero:str,found_hero=False):
    region = Region([343,240,125,385])
    if not standard_run_thread.program_running:
        return
    if GUILDED_HERO !=None and (GUILDED_HERO == hero or hero in GUILDED_HERO_COPIES):
        while True:
            box = ag.locateOnScreen(f"Photos/Heroes/Guilded/{hero}_guilded.png",region=region,confidence=0.75)
            if box == None and not found_hero:
                return None
            elif box == None and found_hero:
                Scroll_Up_fast()
                return Search_latest_hero(hero,found_hero=True)
            else:
                loc_heroname = ((box[0]+box[2]),box[1]+box[3]//2)
                loc_buyhero = (loc_heroname[0]-335,loc_heroname[1]+30)
                return loc_buyhero
    else:
        while True:
            box = ag.locateOnScreen(f"Photos/Heroes/Normal/{hero}.png",region=region,confidence=0.75)
            if box == None and not found_hero:
                return None
            elif box == None and found_hero:
                Scroll_Up_fast()
                return Search_latest_hero(hero,found_hero=True)
            else:
                loc_heroname = ((box[0]+box[2]),box[1]+box[3]//2)
                loc_buyhero = (loc_heroname[0]-335,loc_heroname[1]+30)
                return loc_buyhero


def Check_latest_hero():
    print("Checking latest hero")
    found_hero = False
    Scroll_Bottom()
    for hero in Guilded_heroes[1:Guilded_heroes.index(MAX_HERO)+1][::-1]:
    #for hero in All_Heroes[27:All_Heroes.index(MAX_HERO)+1][::-1]:
        if not standard_run_thread.running:
            break
        if hero == "Betty2" or hero == "King Midas2":
            continue
        print(hero)
        loc = Search_latest_hero(hero,found_hero=found_hero)
        if loc == None:
            pass
        else:
            found_hero = True
            lvl = Get_Lvl(loc)
            if lvl >= Hero_Info[hero][2]:
                print(f"{hero} is at max level. Moving on.")
                return Guilded_heroes.index(hero)+1
    return 0
                


class Fishing(threading.Thread):
    def __init__(self, daemon):
        super(Fishing, self).__init__(daemon=daemon)
        self.running = True
        self.program_running = True
    
    def start_fishing(self):
        self.running = True
    
    def stop_fishing(self):
        self.running = False

    def run(self):
        remaining_time = 0
        global fishing
        fishing = False
        ag.sleep(10)
        while self.program_running:
            while self.running:
                while remaining_time > 0:
                    ag.sleep(1)
                    remaining_time -= 1
                if not self.running:
                    break
                # print("Fishing")
                loc = Find_fish_new()
                if not self.running:
                    break
                if loc is not None:
                    if not self.running:
                        break
                    fishing = True
                    ag.click(loc, _pause=False)
                    ag.sleep(0.1)
                    # print("Fish clicked")
                    fishing = False
                # else:
                #     print("No fish found")
                remaining_time = 60
            ag.sleep(1)
                    

def Init_fishing(daemon:bool=True):
    global fishing_thread
    fishing_thread = Fishing(daemon=daemon)
    fishing_thread.start()


def Start_fishing():
    fishing_thread.start_fishing()
    ag.sleep(0.1)


def Stop_fishing():
    fishing_thread.stop_fishing()
    ag.sleep(0.1)


class Check_Ascend(threading.Thread):
    def __init__(self, daemon):
        super(Check_Ascend, self).__init__(daemon=daemon)
        self.running = True
        self.program_running = True
    
    def start_check_ascend(self):
        self.running = True

    def stop_check_ascend(self):
        self.running = False

    def Ascend(self):
        ascend_region = Region([1192,226,38,38])
        salvage_region = Region([393,240,163,50])
        yes1_region = Region([431,390,163,50])
        yes2_region = Region([498,415,110,50])
        ascend_loc = ag.locateCenterOnScreen("Photos/Buttons/Ascend_button.png",region=ascend_region,confidence=0.75)
        if ascend_loc == None:
            print("Could not find ascend button. Leveling Amenhotep to 150")
            Lvl_Hero_To("Amenhotep",Lvl=150)
            print("Ascending")
            self.Ascend()
        else:
            ag.click(ascend_loc,_pause=False)
            ag.sleep(0.5)
            salvage_loc = ag.locateCenterOnScreen("Photos/Buttons/Salvage_button.png",region=salvage_region,confidence=0.75)
            if salvage_loc:
                yes1_loc = ag.locateCenterOnScreen("Photos/Buttons/Yes_button.png",region=yes1_region,confidence=0.75)
                if yes1_loc:
                    ag.click(yes1_loc,_pause=False)
                    ag.sleep(0.5)
            yes2_loc = ag.locateCenterOnScreen("Photos/Buttons/Yes_button.png",region=yes2_region,confidence=0.75)
            if yes2_loc:
                ag.click(yes2_loc,_pause=False)
                ag.sleep(0.5)
        
    def run(self):
        stuck = False
        remaining_time = 0
        stuck_counter = 0
        Stuck_Zone = -1
        Stuck_zone_previous = -1
        pprint = True
        while self.program_running:
            while self.running:
                while remaining_time > 0:
                    ag.sleep(1)
                    remaining_time -= 1
                if not self.running:
                    break
                if pprint:
                    print(f"Current zone: {Get_Zone()}")
                if Get_Zone() in [Stuck_Zone,Stuck_Zone+1,Stuck_Zone-1,Stuck_zone_previous,Stuck_zone_previous+1,Stuck_zone_previous-1]:
                    stuck_counter += 1
                    if stuck_counter == 1 and IDLE:
                        print("Stuck while idle. Going active")
                        Go_active()
                        stuck_counter = 0
                    elif stuck_counter == 1 and not IDLE and not use_skills_thread.running:
                        print("Stuck while active. Using skills")
                        stuck_counter = 0
                        if EARLY_HEROES_BOUGHT:
                            Start_use_skills()
                    elif stuck_counter == 1 and use_skills_thread.running:
                        print("Stuck!!")
                        stuck = True
                else:
                    stuck_counter = 0
                if stuck and not DEEP_RUN:
                    print("Preparing to Ascend. Ascending in 60 seconds")
                    Stop_standard_run()
                    Stop_use_skills()
                    Stop_auto_progress()
                    ag.sleep(50)
                    countdown = 10
                    while countdown > 0:
                        print(f"Ascending in {str(countdown)} seconds")
                        ag.sleep(1)
                        countdown -= 1
                    Stop_fishing()
                    print("Ascending")
                    ag.sleep(5)
                    global ASCENDING
                    ASCENDING = True
                    self.Ascend()
                    ASCENDING = False
                    Get_new_guilds()
                    Use_calculator()
                    Stuck_Zone = -1
                    Stuck_zone_previous = -1
                    stuck = False
                    use_skills_thread.first_run = True
                    auto_progress_thread.remaining_time = 0
                    Start_auto_progress()
                    Start_fishing()
                    Start_standard_run()
                Stuck_zone_previous = Stuck_Zone
                Stuck_Zone = Get_Zone()
                remaining_time = 30
                if pprint:
                    pprint = False
                else:
                    pprint = True
            ag.sleep(1)


def Init_check_ascend(daemon:bool=True):
    global check_ascend_thread
    check_ascend_thread = Check_Ascend(daemon=daemon)
    check_ascend_thread.start()


def Start_check_ascend():
    check_ascend_thread.start_check_ascend()
    ag.sleep(0.1)


def Stop_check_ascend():
    check_ascend_thread.stop_check_ascend()
    ag.sleep(0.1)


class Clicking(threading.Thread):
    def __init__(self,loc,daemon:bool=True):
        super(Clicking, self).__init__(daemon=daemon)
        self.delay = 0.008 if sys.platform == "darwin" else 0.025
        self.running = False
        self.program_running = True
        self.loc = loc

    def start_clicking(self):
        self.running = True
        
    def stop_clicking(self):
        self.running = False
    
    def run(self):
        pass
        while self.program_running:
            while self.running and not fishing:
                    ag.click(self.loc,_pause=False)
                    ag.sleep(self.delay)
            ag.sleep(0.1)


def Init_autoclicker(loc,daemon:bool=True):
    global click_thread
    click_thread = Clicking(loc,daemon=daemon)
    click_thread.start()
    

def Start_autoclicker():
    click_thread.start_clicking()
    ag.sleep(0.1)
    

def Stop_autoclicker():
    click_thread.stop_clicking()
    ag.sleep(0.1)



class Auto_progress(threading.Thread):
    def __init__(self, daemon):
        super(Auto_progress, self).__init__(daemon=daemon)
        self.running = True
        self.program_running = True
        self.remaining_time = 0
    
    def start_auto_progress(self):
        self.running = True

    def stop_auto_progress(self):
        self.running = False

    def run(self):
        region = Region([1198,183,38,38])
        while self.program_running:
            while self.running:
                while self.remaining_time > 0:
                    ag.sleep(1)
                    self.remaining_time -= 1
                if not self.running:
                    break
                Farmmode_button = ag.locateCenterOnScreen("Photos/Buttons/Farmmode_button.png",region=region,confidence=0.75)
                if Farmmode_button:
                    ag.press("a",_pause=False)
                self.remaining_time = 40
            ag.sleep(1)
                

def Init_auto_progress(daemon:bool=True):
    global auto_progress_thread
    auto_progress_thread = Auto_progress(daemon=daemon)
    auto_progress_thread.start()


def Start_auto_progress():
    auto_progress_thread.start_auto_progress()
    ag.sleep(0.1)


def Stop_auto_progress():
    auto_progress_thread.stop_auto_progress()
    ag.sleep(0.1)


class Use_skills(threading.Thread):
    def __init__(self, daemon):
        super(Use_skills, self).__init__(daemon=daemon)
        self.running = False
        self.program_running = True
        self.first_run = True

    def start_use_skills(self):
        if self.first_run:
            self.run_skills_first_time()
        self.running = True

    def stop_use_skills(self):
        self.running = False

    def run_skills_first_time(self):
        global skill_cooldowns_copy
        global Energized_skills
        for skill in First_run_skills:
            print(skill)
            ag.press(Skill_buttons[skill],_pause=False)
            skill_cooldowns_copy[skill] = skill_cooldowns[skill]
            ag.sleep(0.1)
        Energized_skills["Clickstorm"] = True
        self.skill_timer = min(skill_cooldowns_copy.values())
        self.time1 = time.time()
        self.first_run = False

    def run(self):
        global skill_cooldowns_copy
        global Energized_skills
        while self.program_running:
            while self.running:
                if not self.running:
                    break
                self.time2 = time.time()
                if self.time2-self.time1 > 1:
                    self.skill_timer = int(self.skill_timer-(self.time2-self.time1))
                self.skill_timer_copy = self.skill_timer + 2
                if not self.running:
                    break
                while self.skill_timer_copy > 0:
                    if not self.running:
                        break
                    ag.sleep(1)
                    self.skill_timer_copy -= 1
                for skill in skill_cooldowns_copy:
                    skill_cooldowns_copy[skill] -= self.skill_timer
                for skill in Main_skills:
                    if not self.running:
                        break
                    if skill_cooldowns_copy[skill] <= 0:
                        if Infinite_skills[skill] == False:
                            Energized_skills[skill] = False
                        if skill_cooldowns_copy["Energize"] <= 0 and Energized_skills[skill] == False:
                            ag.press(Skill_buttons["Energize"],_pause=False)
                            skill_cooldowns_copy["Energize"] = skill_cooldowns["Energize"]
                            ag.sleep(0.1)
                            ag.press(Skill_buttons[skill],_pause=False)
                            skill_cooldowns_copy[skill] = skill_cooldowns[skill]
                            ag.sleep(0.1)
                            Energized_skills[skill] = True
                        else:
                            ag.press(Skill_buttons[skill],_pause=False)
                            skill_cooldowns_copy[skill] = skill_cooldowns[skill]
                            ag.sleep(0.1) 
                self.time1 = time.time()
                self.skill_timer = min(skill_cooldowns_copy.values())
                print(f"next skill in {self.skill_timer} seconds")
            ag.sleep(1)
                
    

def Init_use_skills(daemon:bool=True):
    global use_skills_thread
    use_skills_thread = Use_skills(daemon=daemon)
    use_skills_thread.start()


def Start_use_skills():
    use_skills_thread.start_use_skills()
    ag.sleep(0.1)


def Stop_use_skills():
    use_skills_thread.stop_use_skills()
    ag.sleep(0.1)


class Standard_run(threading.Thread):
    def __init__(self, daemon):
        super(Standard_run, self).__init__(daemon=daemon)
        self.running = True
        self.program_running = True

    
    def start_standard_run(self):
        self.running = True
    
    def stop_standard_run(self):
        self.running = False
    
    def exit(self):
        self.program_running = False
        self.running = False

    def run(self):
        global GUILDED_HERO_COPIES
        while self.program_running:
            while self.running:
                print("Starting standard run")
                if not self.program_running:
                    break
                if GUILDED_HERO != None:
                    if not self.program_running:
                        break
                    if GUILDED_HERO == "Samurai":
                        GUILDED_HERO_COPIES = []
                    else:
                        if not self.program_running:
                            break
                        duplicates = Has_duplicates(GUILDED_HERO)
                        if duplicates:
                            GUILDED_HERO_COPIES = duplicates
                        else:
                            GUILDED_HERO_COPIES = []
                        guild_hero(Guilded_heroes[Guilded_heroes.index(GUILDED_HERO)-1])
                if not self.program_running:
                    break
                if START_IDLE:
                    Go_idle()
                else:
                    Go_active()
                if not self.program_running:
                    break
                try:
                    get_skill_timers()
                except:
                    if not self.program_running:
                        break
                    Start_autoclicker()
                    ag.sleep(10)
                    Stop_autoclicker()
                    if not self.program_running:
                        break
                    ag.sleep(5)
                    if not self.program_running:
                        break
                    BuyHero("Treebeast")
                    if not self.program_running:
                        break
                    ag.sleep(10)
                    if not self.program_running:
                        break
                    BuyEarlyHeroes()
                    if not self.program_running:
                        break
                    Lvl_Hero_To(Guilded_heroes)
                Lvl_Hero_To(Guilded_heroes[Check_latest_hero():])
            ag.sleep(0.1)


def Init_standard_run(daemon:bool=False):
    global standard_run_thread
    standard_run_thread = Standard_run(daemon=daemon)
    standard_run_thread.start()

    def Exit_standard_run():
        print("Exiting program")
        standard_run_thread.exit()
        listener.stop()
        ag.sleep(0.1)

    def for_canonical(f):
        return lambda k: f(listener.canonical(k))

    end_hotkey = HotKey(HotKey.parse('<shift>+q'), on_activate=Exit_standard_run)
    with Listener(on_press=for_canonical(end_hotkey.press),on_release=for_canonical(end_hotkey.release)) as listener:
        listener.join()


def Start_standard_run():
    standard_run_thread.start_standard_run()
    ag.sleep(0.1)


def Stop_standard_run():
    standard_run_thread.stop_standard_run()
    ag.sleep(0.1)                 




    


def Start_background_processes():
    Start_fishing()
    Start_auto_progress()
    Start_check_ascend()
    

def Stop_background_processes():
    Stop_fishing()
    Stop_auto_progress()
    Stop_check_ascend()


def Initialize_program():
    os.system("clear")
    global model
    import pathlib
    pathlib.PosixPath = pathlib.WindowsPath
    model = torch.hub.load("yolov5", 'custom', path=os.path.join('yolov5', 'runs', 'train', '300_hpc', 'weights', 'best.pt'), source='local',device='cpu')
    global pause
    if sys.platform == "darwin":
        pause = False
    else:
        pause = True
    FocusWindowAndGetWindowPOS()
    Init_autoclicker((950+offsetx,350+offsety))
    Init_fishing()
    Init_auto_progress()
    Init_use_skills()
    Init_check_ascend()
    Init_standard_run() # Main run.
