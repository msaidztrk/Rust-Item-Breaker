import time
import cv2
import numpy as np
from PIL import ImageGrab
import glob
import os
import pyautogui
import sys

def find_and_click(image_paths, threshold=0.8):
    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

    for image_path in image_paths:
        template = cv2.imread(image_path, 0)
        if template is None:
            continue

        w, h = template.shape[::-1]
        res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        if loc[0].size > 0:
            pt = (loc[1][0], loc[0][0])
            center_x = pt[0] + w // 2
            center_y = pt[1] + h // 2
            pyautogui.click(center_x, center_y)
            print(f"Clicked on {os.path.basename(image_path)}")
            return True
            
    return False

def main():
    item_folder = 'rust-item-imgs'
    btn_folder = 'btn-imgs'
    
    item_image_paths = glob.glob(os.path.join(item_folder, '*.png'))
    breakdown_image_paths = [os.path.join(btn_folder, 'breakdown.png')]
    confirm_btn_path = [os.path.join(btn_folder, 'confirm.png')]

    if not item_image_paths:
        print(f"No item images found in '{item_folder}' directory.")
        sys.exit()

    while True:
        print("Searching for an item to break...")
        if find_and_click(item_image_paths):
            print("Item found and clicked. Waiting to find breakdown button...")
            time.sleep(3)
            
            if find_and_click(breakdown_image_paths):
                print("Breakdown button clicked. Waiting to find confirm button...")
                time.sleep(2)

                if find_and_click(confirm_btn_path):
                    print("Confirm button clicked. Restarting loop.")
                else:
                    print("Confirm button not found. Restarting loop.")
            else:
                print("Breakdown button not found. Restarting loop.")
        else:
            print("No matching item images found on screen. Retrying...")
        
        time.sleep(1) # Add a small delay before the next loop iteration

if __name__ == "__main__":
    main()
