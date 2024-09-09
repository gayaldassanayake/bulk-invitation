import csv
import os
from PIL import Image, ImageFont, ImageDraw 
 
with open('invitations.csv', mode ='r') as file:
  reader = csv.reader(file)
  font = ImageFont.truetype('fonts/AlexBrush.ttf', 40)

  for value in reader:
    name = value[0]
    group = value[1]
    invitation = Image.open("invitation.png")
    editable = ImageDraw.Draw(invitation)

    image_width, image_height = invitation.size
    
    text_bbox = editable.textbbox((0, 0), name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    
    x_position = (image_width - text_width) // 2
    y_position = 1510

    editable.text((x_position, y_position), name, (0, 0, 0), font=font)
    pngDir = "exports/png"
    targetDir = "exports/" + group
    os.makedirs(targetDir, exist_ok=True)
    os.makedirs(pngDir, exist_ok=True)


    invitation.save(pngDir + "/"+ name + ".png")
    invitation.save(targetDir + "/"+ name + ".pdf", "PDF", resolution=300.0)


