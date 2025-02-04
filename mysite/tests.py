import cv2
from pyzbar.pyzbar import decode

image = cv2.imread('static/IMG_0498.JPG')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
decoded_objects = decode(gray_image)



for obj in decoded_objects:
    print('Type:', obj.type)
    print('Data:', obj.data.decode('utf-8'))


