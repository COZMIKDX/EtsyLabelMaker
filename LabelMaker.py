import PySimpleGUI as sg
#import os, sys
from PIL import Image, ImageFont, ImageDraw
import io

#Select output location. Filename based on first line of input.
#Paste the four lines of text into the input text box.
# Press make label button to save the file.
# Maybe display a preview of the label. Indicate to the user that the label is saved.
##############################################################################

# Label image setup
font = ImageFont.truetype("PTSerif-Regular.ttf", 50)
# blank image
im = Image.new(mode="RGB", size = (1920,1280), color = (255,255,255))
# editable object representing image.
editable_image = ImageDraw.Draw(im)

# Setting up blank thumbnail for window launch
im_thumbnail = im.copy()
im_thumbnail.thumbnail((320, 160))
temp = io.BytesIO()
im_thumbnail.save(temp, format = "png")

# GUI setup
sg.theme('Dark2')

layout = [
    [sg.Text('Enter address info')],
    [sg.Multiline(size = (30,5), key='textbox'), sg.Image(key='labelpic')],
    [sg.Button('Make label')]
]

window = sg.Window('Shipping Label Maker', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    window['labelpic'].update(temp.getvalue())
    print(event, values)
    if event == "Make label":
        editable_image.text((500,500), values['textbox'], font = font, fill=(0,0,0,255), spacing=20)
        im_thumbnail = im.copy()
        im_thumbnail.thumbnail((320, 160))
        temp = io.BytesIO()
        im_thumbnail.save(temp, format = "PNG")

        #window['labelpic'].update(temp.getvalue())
        im.save("test.png")


window.close()