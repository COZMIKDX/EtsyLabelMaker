import PySimpleGUI as sg
from PIL import Image, ImageFont, ImageDraw
import io
import os

#TODO: Make a way for the user to add multiple addresses to a single label.
# I could either have the user add addresses without checking if it fits on the label.
# The user could look at the preview to see if it all fits okay.
# Each new address would be added below the previous and then start at the top to the right.
# Checking if the whole address fits might be a bit difficult since I'd have to figure out how to calculate the size
# of the text input on the fly.
# I could give each address the user inputs a set of (x,y) coords that they can manipulate themselves so that they
# can place them however they want on the label, using the preview to make sure that's what they want.

font = ImageFont.truetype("PTSerif-Regular.ttf", 50)

## Image stuff
thumbnail_width = 320
thumbnail_height = 160

# Blank image so the thumbnail portion of the GUI is not empty initially.
im_thumbnail = Image.new(mode="RGB", size = (1920,1280), color = (255,255,255))
im_thumbnail.thumbnail((320, 160))
temp = io.BytesIO() # used to hold the image data temporarily without saving it to a file.
im_thumbnail.save(temp, format="PNG")


## Address stuff
class Address:
    def __init__(self, info, x, y):
        self.info = info.split('\n')
        self.x = x
        self.y = y



address_list = []


def add_address(info, x, y):
    global address_list
    address_list.append(Address(info, x, y))

# TODO: figure out indexing the addresses in the address list. This should also be useful for displaying and editing.
def delete_address(index):
    global address_list
    address_list.pop(index)


def list_addresses():
    global address_list
    address_first_lines = [entry.info[0] for entry in address_list]
    return address_first_lines


def load_address():
    pass


# GUI setup
sg.theme('Dark2')

col0 = [
    [sg.Text('Enter address info:')],
    [sg.Multiline(size=(30,5), key='textbox')],
    [sg.DropDown(key='address list',size=(30,5), values=[], readonly=True)],
    [sg.Text('Start position:')],
    [sg.Text('x:'), sg.InputText(key='x_coord', size=(8,1), default_text='0'), sg.Text('y:'), sg.InputText(key='y_coord', size=(8,1), default_text='0')],
    [sg.Button('Save new address'), sg.Button('Save as edit', disabled=True), sg.Button('Delete Address')],
    [sg.Button('Make label'), sg.FolderBrowse(key='browse', button_text='Choose save location')],
    [sg.Text('Status: '), sg.Text('', key='outputindicator')]
]
col1 = [[sg.Image(temp.getvalue(), key='labelpic')]]

layout = [[
    sg.Column(col0), sg.Column(col1)
]]

window = sg.Window('Shipping Label Maker', layout)

x_coord = 0
y_coord = 0


def coordinate_error_check(x, y):
    global window
    global x_coord
    global y_coord

    # Error checking the x and y coordinate input
    # Check for integers and then if the coordinates are on the label.
    integer_coords = True
    coord_in_bounds = True
    coord_check_passed = True
    if not x.isdigit() or not y.isdigit():
        integer_coords = False

    #if coords are not in bounds:
    #   coord_in_bounds = False

    if not (integer_coords and coord_in_bounds):
        coord_check_passed = False
        window['outputindicator'].update('Integer coordinates only')
    else:
        window['outputindicator'].update('')


    return coord_check_passed


def coordinate_assign(x, y):
    global x_coord
    global y_coord
    if coordinate_error_check(x, y):
        x_coord = int(x)
        y_coord = int(y)
    else:
        x_coord = 0
        y_coord = 0


def thumbnail_preview(im):
    im_thumbnail = im.copy()
    im_thumbnail.thumbnail((320, 160))
    temp = io.BytesIO()
    im_thumbnail.save(temp, format = "PNG")
    return temp




# Event loop
while True:
    event, values = window.read(timeout=250)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event != '__TIMEOUT__':
        print(event, values)

    coordinate_assign(values['x_coord'], values['y_coord'])

    # Making a preview thumbnail.
    # Create a blank image, make it editable, stick the text from the textbox at the moment on the image,
    # Make a thumbnail out of the image.
    im = Image.new(mode="RGB", size = (1920,1280), color = (255,255,255))
    editable_im = ImageDraw.Draw(im)
    editable_im.text((x_coord, y_coord), values['textbox'], font = font, fill=(0,0,0,255), spacing=20)

    # Make thumbnail and update window
    thumbnail = thumbnail_preview(im)
    window['labelpic'].update(thumbnail.getvalue())

    # Attempt to save the label.
    if event == "Make label":
        address_info = values['textbox'].split('\n')
        if values['browse'] == '':
            window['outputindicator'].update("Select a save location!")
        else:
            # TODO Check for potential duplicates and change file name.
            im.save(values['browse'] + os.path.sep + address_info[0] + '.png') # Make the filename the first line. Typically that's the recipient's name.
            window['outputindicator'].update("Saved " + address_info[0] + ".png")
    if event == "Save new address":
        add_address(values['textbox'], x_coord, y_coord)
        print(address_list)
        window['address list'].update(values=list_addresses())


window.close()