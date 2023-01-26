import math
import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import keyboard

def find_and_shoot_birds():
    """ Captures screen, template matches birds and clicks the matched location """
    isRunning = False

    screenTOP = 104
    screenBOT = 460
    screenLFT = 2
    screenRGT = 670

    template = cv2.imread('img/beak.png', 0)
    template_w, template_h = template.shape[::-1]

    abs_x = screenLFT
    abs_y = screenTOP
    
    bullet_count = 0
    reload = 12

    #framecount = 0
    while (True):

        if keyboard.is_pressed("s"):
            continue

        #framecount += 1
        #if ((framecount % 5) != 0):
        #    continue
        #if keyboard.is_pressed("s"):
        #    isRunning = not isRunning

        #if not isRunning:
        #    continue

        # Read screen
        frame_bgr = np.array(ImageGrab.grab(bbox=(screenLFT, screenTOP, screenRGT, screenBOT)))

        # Convert to gray
        frame_gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

        # Apply template Matching
        bird_candidates = cv2.matchTemplate(image=frame_gray, templ=template, method=cv2.TM_CCOEFF_NORMED)
        definite_birds = np.where(bird_candidates >= 0.7)

        if keyboard.is_pressed("d"):
            #print("D PRESSED")
            for bird in zip(*definite_birds[::-1]):
                cv2.circle(img=frame_bgr, center=(int(bird[0] + template_w/2), int(bird[1] + template_h / 2)), radius=int(template_h/2), color=(255, 0, 0), thickness=2)
                cv2.drawMarker(img=frame_bgr, position=(int(bird[0] + template_w/2), int(bird[1] + template_h / 2)),color=(255, 0, 0), markerType=cv2.MARKER_CROSS, markerSize=30, thickness=2, line_type=cv2.LINE_4)

                cv2.imshow('Duck Hunt', cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))

                if (cv2.waitKey(30) == 27):
                    cv2.destroyAllWindows()
                    break

        just_shot_coords = []
        for bird in zip(*definite_birds[::-1]):
            abs_x = int(bird[0]) + screenLFT
            abs_y = int(bird[1]) + screenTOP

        # Check if the target is close to somewhere whe just shot
        #too_close = False
        #for jsa in just_shot_coords:
        #    dist = math.dist(jsa, [abs_x, abs_y])
        #    if (dist < min([template_w, template_h])):
        #        too_close = True
        #        break
        #if (too_close):
        #    continue

        # Shoot!
        if (abs_x != screenLFT):
            pyautogui.click(abs_x, abs_y)
            just_shot_coords.append((abs_x, abs_y))
            bullet_count += 1

            if bullet_count == reload:
                pyautogui.press("space")
                bullet_count = 0 

        if keyboard.is_pressed("p"):
            reload += 1
        
        #cv2.imshow('Duck Hunt', cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))

        #if (cv2.waitKey(30) == 27):
        #    cv2.destroyAllWindows()
        #    break


find_and_shoot_birds()