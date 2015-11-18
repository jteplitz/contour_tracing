from PIL import Image
import os

path = os.path.dirname(os.path.abspath(__file__ ))
path += "/../images/rishi1.jpg"
im = Image.open(path)
#im.show()

print(im.format, im.size, im.mode)
#print (im.histogram())
#print (im.getpixel((0, 0)))
