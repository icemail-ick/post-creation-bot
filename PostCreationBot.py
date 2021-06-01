import io
import os
from numpy import random
from google.cloud import vision_v1
from PIL import Image, ImageFont, ImageDraw
# from Pillow_Utility import draw_borders, Image
import sys
import pandas as pd
import json

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"SecretAccountKey.json"
client = vision_v1.ImageAnnotatorClient()

file_name = "unnamed.png"
image_path = os.path.join('./Images', file_name)

im = Image.open(image_path)

with io.open(image_path, 'rb') as image_file:
    content = image_file.read()

image = vision_v1.types.Image(content=content)
response = client.object_localization(image=image)
localized_object_annotations = response.localized_object_annotations


sys.argv = im

blank = Image.open(image_path)
pixels = []
while len(pixels):
    x = random.randint(0, blank.size[0] - 1)
    y = random.randint(0, blank.size[1] - 1)
    pixel = blank.getpixel((x, y))
    if pixel[-1] > 200:
        pixels.append(((x, y), pixel[:-1]))


def diff(a, b):
    return sum((a - b) ** 2 for a, b in zip(a, b))


best = []

for x in range(im.size[0]):
    for y in range(im.size[1]):
        d = 0
        for coor, pixel in pixelt:
            try:
                ipixel = im.getpixel((x + coor[0], y + coor[1]))
                d += diff(ipixel, pixel)
            except IndexError:
                d += 256 ** 2 * 3
        best.append((d, x, y))
        best.sort(key=lambda x: x[0])
        best = best[:3]


# detectedObjects = []


# class pixelPoint:
#      def __init__(self, x, y):
#          self.x = x
#          self.y = y


# class detectedObject:
#     def __init__(self, name):
#         self.name = name
#         self.points = pixelPointsArray

# detObj = json.dumps(localized_object_annotations)


# for obj in localized_object_annotations:
#     currentObject = setattr(detectedObject, "name", obj.name)
#     pixelPointsArray = []
#     # print(obj.bounding_poly.normalized_vertices)
#     for nv in obj.bounding_poly.normalized_vertices:
#         setattr(pixelPoint, "x", nv.x)
#         setattr(pixelPoint, "y", nv.y)
#         pixelPointsArray.append(pixelPoint)
#     setattr(detectedObject, 'points',pixelPointsArray )
#     detectedObjects.append(detectedObject)
#     # print(obj)

# for detObj in detectedObjects:
#     print(detObj)


df = pd.DataFrame(columns=['name', 'score', 'value'])
for obj in localized_object_annotations:
    df = df.append(
        dict(
            name=obj.name,
            score=obj.score,

        ),
        ignore_index=True)

pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]


width, height = im.size
image_editable = ImageDraw.Draw(im)
title_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/freefont/FreeMono.ttf", 12, encoding="unic")
title_text = "The Beauty of Nature"
draw_txt = ImageDraw.Draw(im)
width, height, = draw_txt.textsize(title_text, font=title_font)

print(df)

image_editable.text((10, 10), title_text, (237, 230, 211), font=title_font)
im.save("result.jpg")





