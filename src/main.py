import RPi.GPIO as GPIO
import time
import subprocess
from crop import cropImg
import cv2
from feature_extractor import bvgFeatureExtractor

BASE_PATH = "/home/pi/bvg_data"

BUTTON_PIN = 7;
DELAY = 0.25;

SHUTTER_SPEED = 4000
CONTRAST = 100
EV = 0

GPIO.setmode(GPIO.BOARD)

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    if (GPIO.input(BUTTON_PIN)):
        print("Taking picture")
        #subprocess.call("./picture.sh", shell=True)
        fileName = str(time.time()) + ".jpg"
        filePath = BASE_PATH + "/input_images/" + fileName
        print(filePath)
        subprocess.call(["raspistill", "-ex", "fixedfps", "-ss", str(SHUTTER_SPEED), "-co",
                        str(CONTRAST),
                        "-ev", str(EV), "-o", filePath, "-n"])
        print("Picture taken")
        croppedImg = cropImg(filePath)
        croppedFilePath = BASE_PATH + "/cropped_images/" + fileName
        cv2.imwrite(croppedFilePath, croppedImg)
        print(croppedFilePath)
        print("Image cropped")
        featureFilePath = BASE_PATH + "/features/" + fileName[:-4] + ".csv"
        command = ["octave", "/home/pi/contour_tracing/matlab/extract_features.m", croppedFilePath, featureFilePath]
        command = " ".join(command)
        subprocess.call("/bin/su - pi -c \"" + command + "\"", shell = True)
        print("Feature file created")
        bvgFeatureExtractor(featureFilePath, intersections=False, fuzzy_grid=True, vein_angles=False, avg_angles=False, rishi_angles=False, up_down=True, print_advanced_features=True, midpoint_veins=True)
    time.sleep(DELAY)
