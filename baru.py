import io
import os
from numpy import random
from google.cloud import vision_v1
from PIL import Image, ImageFont, ImageDraw
# from Pillow_Utility import draw_borders, Image
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


# def main():  {

#     file_name = "unnamed.png"
#     image_path = os.path.join('./Images', file_name)
#
#     im = Image.open(image_path)
# 
#     size = width, height=image.size


# }


class pixelPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class detectedObject:
    def __init__(self, name):
        self.name = name
        self.points = pixelPointsArray


detObj = json.dumps(localized_object_annotations)


for obj in localized_object_annotations:
    currentObject = setattr(detectedObject, "name",
                            obj.name, "bounding_poly", obj.bounding_poly)
    pixelPointsArray = []
    # print(obj.bounding_poly.normalized_vertices)
    for nv in obj.bounding_poly.normalized_vertices:
        setattr(pixelPoint, "x", nv.x)
        setattr(pixelPoint, "y", nv.y)
        pixelPointsArray.append(pixelPoint)
    setattr(detectedObject, 'points', pixelPointsArray)
    detectedObjects.append(detectedObject)
    print(obj)

pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

print(response)
print(width)
print(height)

df = pd.DataFrame(columns=['name', 'bounding_poly', 'normalized_vertices'])
for obj in localized_object_annotations:
    df = df.append(
        dict(
            name=obj.name,
            bounding_poly=obj.bounding_poly.normalized_vertices,
            normalized_vertices=obj.bounding_poly.normalized_vertices,
        ),
        ignore_index=True)


class Object:
    def __init__(self, name, posisi):
        self.name = name
        self.posisi = posisi

#p1 = Object()
#p1.name = "x"
#p1.posisi = 36

#p2 = Object()
#p2.name = "y"
#p2.posisi = 30


p1 = Object("x", 36)
p2 = Object("y", 30)

p1 = Object(x, posisi)

print(p1.posisi + p2.posisi)

arr = []

i = 1
for i in range(4):
    arr.append(Object("x"+str(i), 36))


width, height = im.size

# for detObj in detectedObjects:
#     print(detObj)


# pixels = list(im.getdata())
# width, height = im.size
# pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]


# width, height = im.size
# image_editable = ImageDraw.Draw(im)
# title_font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 12, encoding="unic")
# title_text = "The Beauty of Nature"
# draw_txt = ImageDraw.Draw(im)
# width, height, = draw_txt.textsize(title_text, font=title_font)


# image_editable.text((15,15), title_text, (237, 230, 211), font=title_font)
# im.save("result.jpg")

# print(df)

# print(df.values)
