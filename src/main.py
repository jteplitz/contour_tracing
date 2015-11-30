import RPi.GPIO as GPIO
import time
import subprocess
from crop import cropImg
import cv2

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
        print("Image cropped")
        featureFilePath = BASE_PATH + "/features/" + fileName[:-4] + ".csv"
        subprocess.call(["octave", "../matlab/extract_features.m", croppedFilePath, featureFilePath])
    time.sleep(DELAY)
