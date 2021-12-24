import PySimpleGUI as sg
from PIL import Image, ImageFont, ImageDraw
import io
import os


font = ImageFont.truetype("PTSerif-Regular.ttf", 50)

# Blank image so the thumbnail portion of the GUI is not empty initially.
im_thumbnail = Image.new(mode="RGB", size = (1920,1280), color = (255,255,255))
im_thumbnail.thumbnail((320, 160))
temp = io.BytesIO() # used to hold the image data temporarily without saving it to a file.
im_thumbnail.save(temp, format="PNG")

# GUI setup
sg.theme('Dark2')

layout = [
    [sg.Text('Enter address info:')],
    [sg.Multiline(size = (30,5), key='textbox'), sg.Image(temp.getvalue(), key='labelpic')],
    [sg.Button('Make label'), sg.FolderBrowse(key='browse', button_text='Choose save location'), sg.Text('', key='outputindicator')]
]

window = sg.Window('Shipping Label Maker', layout)


# Event loop
while True:
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event != '__TIMEOUT__':
        print(event, values)

    # Making a preview thumbnail.
    # Create a blank image, make it editable, stick the text from the textbox at the moment on the image,
    # Make a thumbnail out of the image.
    im = Image.new(mode="RGB", size = (1920,1280), color = (255,255,255))
    editable_im = ImageDraw.Draw(im)
    editable_im.text((500,500), values['textbox'], font = font, fill=(0,0,0,255), spacing=20)
    im_thumbnail = im.copy()
    im_thumbnail.thumbnail((320, 160))
    temp = io.BytesIO()
    im_thumbnail.save(temp, format = "PNG")

    # update the window to show the new preview.
    window['labelpic'].update(temp.getvalue())

    # Attempt to save the label.
    if event == "Make label":
        address_info = values['textbox'].split('\n')
        if values['browse'] == '':
            window['outputindicator'].update("Select a save location!")
        else:
            #TODO Check for potential duplicates and change file name.
            im.save(values['browse'] + os.path.sep + address_info[0] + '.png') # Make the filename the first line. Typically that's the recipient's name.
            window['outputindicator'].update("Saved " + address_info[0] + ".png")


window.close()