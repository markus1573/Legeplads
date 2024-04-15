from Functions import *

All_ims = glob.glob("Photos/Temp/*.png")
All_ims = sorted(All_ims,key = os.path.getmtime)

for i,path in enumerate(All_ims):
    im = cv2.imread(path)
    cv2.imwrite(f"Photos/Guilds/Guilded/{All_Heroes[i+1]}_guilded.png",im)

