import cv2
import numpy as np
from PIL import ImageGrab
import glob
import os
import pyautogui
import time
import random

# Function to find and click on a random image from the screenshot
def find_and_click_random(template_paths, screenshot):
    # Convert the screenshot to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    
    # Initialize list to store all found locations
    found_locations = []

    # Process each template image
    for template_path in template_paths:
        # Load the template image
        template = cv2.imread(template_path, 0)
        template_height, template_width = template.shape

        # Perform template matching
        result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)

        # Define a threshold for matching
        threshold = 0.8
        loc = np.where(result >= threshold)

        # Store all found locations
        for pt in zip(*loc[::-1]):
            found_locations.append(pt)

    # If locations were found, click on a random location
    if found_locations:
        pt = random.choice(found_locations)
        template_width, template_height = template.shape[::-1]  # Get template dimensions
        center_x = pt[0] + template_width // 2
        center_y = pt[1] + template_height // 2
        pyautogui.click(center_x, center_y)
        cv2.rectangle(screenshot, pt, (pt[0] + template_width, pt[1] + template_height), (0, 0, 255), 2)
        return True  # Indicate that a match was found and clicked

    return False  # No match found

# Function to continuously check for break images on the screen and click them

stop_wait_for_break_img_count = 0
def wait_and_click_break_images(break_image_paths): 
    global stop_wait_for_break_img_count 

    screenshot = np.array(ImageGrab.grab())
    for break_image_path in break_image_paths:
        found = find_and_click_random([break_image_path], screenshot)
    
    if not found:
        print("No break image found")


# Folder containing the images to look for
image_folder = 'rust-item-imgs'  # replace with your folder path
image_paths = glob.glob(os.path.join(image_folder, '*.png'))

# Images to check after the first click
break_into_wood_img = os.path.join(image_folder, 'break-wood.png')
break_into_cloth_img = os.path.join(image_folder, 'break-cloth.png')

count_while = 0
while True:
    screenshot = np.array(ImageGrab.grab())

    # Click on a random detected image
    if find_and_click_random(image_paths, screenshot):
        print('Clicked on a random image')
    else :
        print('No random image detected')

    # Wait for specific images to appear and click them
    time.sleep(2)
    wait_and_click_break_images([break_into_wood_img, break_into_cloth_img])
    time.sleep(2)

    count_while += 1
    print('count_while:', count_while)

# Save and display the output image
output_path = 'output.png'
cv2.imwrite(output_path, screenshot)
# cv2.imshow('Detected Image', screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()
