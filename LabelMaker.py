import PySimpleGUI as sg
from PIL import Image, ImageFont, ImageDraw
import io

font = ImageFont.truetype("PTSerif-Regular.ttf", 50)

## Image stuff
thumbnail_width = 320
thumbnail_height = 160
image_height = 1280
image_width = 1920
bg_color = (255, 255, 255)

# Blank image so the thumbnail portion of the GUI is not empty initially.
im_thumbnail = Image.new(mode="RGB", size=(image_width, image_height), color=bg_color)
im_thumbnail.thumbnail((320, 160))
temp = io.BytesIO()  # used to hold the image data temporarily without saving it to a file.
im_thumbnail.save(temp, format="PNG")


## Address stuff
class Address:
    def __init__(self, info, x, y):
        self.info = info #.split('\n')
        self.x = x
        self.y = y


address_list = []


def add_address(info, x, y):
    global address_list
    address_list.append(Address(info, x, y))


def list_recipients():
    global address_list
    address_first_lines = [entry.info[0] for entry in address_list]
    return address_first_lines



# GUI setup
sg.theme('Dark2')

col0 = [
    [sg.Text('Enter address info:')],
    [sg.Multiline(size=(30, 5), key='textbox')],
    [sg.Text('Start position:')],
    [sg.Text('x:'), sg.InputText(key='x_coords', size=(8, 1), default_text='0'), sg.Text('y:')],
    [sg.Slider(key='x_coord', range=(0, image_width), orientation='h', size=(26, 20), default_value=25)],
    [sg.Slider(key='y_coord', range=(0, image_height), orientation='h', size=(26, 20), default_value=25)],
    [sg.Button('Add', key='AddAddress'), sg.Input(key='FileSave', enable_events=True, visible=False, disabled=True),
     sg.FileSaveAs(button_text='Save', file_types=(("Image Files", "*.png"),))],
    [sg.Text('Info: '), sg.Text('', key='outputindicator')]
]
col1 = [
    [sg.Text("Preview:")],
    [sg.Image(temp.getvalue(), key='labelpic')]
]

layout = [[
    sg.Column(col0), sg.Column(col1)
]]

window = sg.Window('Shipping Label Maker', layout)

x_coord = 0
y_coord = 0


def coordinate_assign(x, y):
    global x_coord
    global y_coord
    x_coord = int(x)
    y_coord = int(y)

def update_image():
    output_im = Image.new(mode="RGB", size=(image_width, image_height), color=bg_color)
    editable_im = ImageDraw.Draw(output_im)
    for address in address_list:
        editable_im.text((address.x, address.y), address.info, font=font, fill=(0, 0, 0, 255), spacing=20)
    editable_im.text((values["x_coord"], values["y_coord"]), values["textbox"], font=font, fill=(0, 0, 0, 255), spacing=20)
    return output_im

def thumbnail_preview(im):
    im_thumbnail = im.copy()
    im_thumbnail.thumbnail((320, 160))
    temp = io.BytesIO()
    im_thumbnail.save(temp, format="PNG")
    return temp



# Event loop
while True:
    event, values = window.read(timeout=250)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event != '__TIMEOUT__':
        print(event, values)

    # Apply the coordinates to the current text.
    coordinate_assign(int(values['x_coord']), values['y_coord'])

    # Create the new image and make it editable. Apply our text to the new image.
    im = update_image()

    # Make thumbnail using updated image and update the window to show it.
    thumbnail = thumbnail_preview(im)
    window['labelpic'].update(thumbnail.getvalue())

    if event == "AddAddress":
        add_address(values["textbox"], values["x_coord"], values["y_coord"])
        window["textbox"].update(value="")

    # Save label as image.
    if event == "FileSave":  # if event == "Make label":
        address_info = values['textbox'].split('\n')
        print("rer")

        # Save image if the file save path is not empty.
        if values["FileSave"] != "":
            image_save_path = values["FileSave"]
            im.save(image_save_path)
            window['FileSave'].update("")

window.close()
