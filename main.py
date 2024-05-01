import time
import cv2 
import numpy as np
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import win32gui
import win32ui
import win32con
import win32api
import keyboard
#####################
# SETTINGS for button to be pressed
#####################
npc = 's'
confidence = 0.6 # set higher if too much false positives, lower if too much false negatives, 0 to 1
sleepAfterSuccess = 0.2 # increase if the AI becomes trigger happy and presses button immediately at the start of each round

#####################
# SETTINGS for game
#####################
hwnds = []
#default size
w = 2560
h = 1440

def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        if (win32gui.GetWindowText(hwnd) == "MapleStory"):
            print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )
            hwnds.append(hwnd)

####################
# PREDICTION LOOP
####################
win32gui.EnumWindows( winEnumHandler, None )
hwnd = hwnds[0]
if (len(hwnds) > 1): #player has chat external
    hwnd = hwnds[1]

#get the correct size
# rect = win32gui.GetWindowRect(hwnd)
# x = rect[0]
# y = rect[1]
# w = rect[2] - x
# h = rect[3] - y

wDC = win32gui.GetWindowDC(hwnd)
dcObj=win32ui.CreateDCFromHandle(wDC)
cDC=dcObj.CreateCompatibleDC()
dataBitMap = win32ui.CreateBitmap()
dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
cDC.SelectObject(dataBitMap)

def start():
    #init yolov8
    model = YOLO('vdanceprops.pt')
    while True: 
        success = False
        start = time.time()
    # Capture frame-by-frame
        cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
        signedIntsArray = dataBitMap.GetBitmapBits(True)

        # #4 channel to 3 channel
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (h,w,4)
        # img = img[:shapeHeight, :w]
        frame = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

        #make the frame half size
        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        
        # Press Q on keyboard to exit 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            dcObj.DeleteDC()
            cDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, wDC)
            win32gui.DeleteObject(dataBitMap.GetHandle())
            cv2.destroyAllWindows() 
            break

        results = model(frame, verbose=False, conf=confidence)
        #get the result boxes
        
        successBox = None
        propsBox = None

        for r in results:
            annotator = Annotator(frame)
            boxes = r.boxes
            #this is for debugging
            for box in boxes:
                b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                c = box.cls
                annotator.box_label(b, model.names[int(c)])
                if model.names[int(c)] == 'success':
                    successBox = b
                    # keyboard.press(npc)
                    # time.sleep(0.1)
                    # keyboard.release(npc)
                if model.names[int(c)] == 'props':
                    propsBox = b

        if successBox is not None and propsBox is not None:
            propBoxCenter = (propsBox[0] + propsBox[2])/2

            # if the propsBox's x center is within success box x left and x right
            if successBox[0] < propBoxCenter and propBoxCenter < successBox[2]:
                print("Succeeding")
                success = True
                keyboard.press(npc)
                time.sleep(0.1)
                keyboard.release(npc)
            

        frame = annotator.result()
        cv2.imshow('Frame', frame)
        end = time.time()
        #sleep for 1/60th of a second minus the time taken to capture the screen
        # sleeptime = 1/60 - (end-start)
        # if sleeptime > 0:
        #     time.sleep(sleeptime)
        
        if success:
            time.sleep(sleepAfterSuccess)
            success = False

start()