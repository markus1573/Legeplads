from Functions import *
from Autoclicker import*
import sys
if sys.platform == "win32":
    os.chdir("C:/Users/marku/Documents/GitHub/Legeplads/Clicker heroes stuff")
elif sys.platform == "darwin":
    os.chdir("/Users/markus/Documents/Legeplads/Clicker heroes stuff")
# os.chdir("Clicker heroes stuff")
MAX_HERO = "Moeru"
GUILDED_HERO = "Tsuchi"
DEEP_RUN = False
START_IDLE = True
if __name__ == '__main__':
    Initialize_program()
    

    # FocusWindowAndGetWindowPOS()
    
    # if sys.platform == "win32":
    #     needleHeight = needleHeight // 2
    #     needleWidth = needleWidth // 2
    #     needleImage = cv2.resize(needleImage, (needleWidth, needleHeight))
