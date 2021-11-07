import cv2
import time
inicio = time.time()

import PIL
from PIL import ImageDraw
import easyocr
from googletrans import Translator
translator = Translator()


img = PIL.Image.open("RES1.jpg")

reader = easyocr.Reader(['ar']) # this needs to run only once to load the model into memory

bounds = reader.readtext(img)
print(bounds)
# Draw bounding boxes
def draw_boxes(image, bounds, color='red', width=2):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        # leng = translator.detect(bound[1])
        #if (leng.lang == 'ar'):
        p0, p1, p2, p3 = bound[0]
        print(bound[1])
        draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)

    return image

draw_boxes(img, bounds).show()

fin = time.time()
print(fin-inicio)
