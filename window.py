import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
from PIL import Image


def make_window(mode):

    sg.theme('DarkAmber')
    #background_color = '#dddddd'
    background_color = '#2c2825'

    slider_res_range = (4, 256)
    slider_col_range = (1, 64)

    if mode == '4k':
        size_control_column = (460, 750)
        size_main_image = (1024, 1024)
        size_color_image = (110, 110)
        size_col_column = (200, 650)
        size_window = (1270, 550)
        font = 'Helvetica 12'
    else:   # Standard Full HD. Everything / 2
        """ WIP """
        size_control_column = (500, 650)
        size_main_image = (512, 512)
        size_color_image = (110, 110)
        size_col_column = (200, 650)
        size_window = (1270, 620)
        font = 'Helvetica 6'

    control_col = sg.Column(layout=[
        [sg.Text('', key='FILLER_1', size=(1, 1), expand_y=False)],
        [sg.Text('Original image resolution: ', ), sg.Text('', key='INFO_ORIGINAL_RES')],
        [sg.Frame('Settings', expand_x=True, layout=[
            #[sg.Button('Select Image', key='SELECT')],
            [sg.FileBrowse("Select Image", key='SELECT', enable_events=True)],
            [sg.Text('', key='FILLER_3', size=(1, 1), expand_y=False)],
            [sg.Checkbox('Keep Ratio', key='BUTTON_RATIO', default=True, enable_events=True)],
            [sg.Text('\nx resolution: ', size=(10, 2)),
             sg.pin(sg.Input(size=(5, 1), key='INPUT_X', enable_events=True, expand_x=False, visible=True), vertical_alignment='b', ),
             sg.Button('', key='ENTER_RES', bind_return_key=True, visible=False),
             sg.Slider(size=(15, 16), key='SLIDER_X', range=slider_res_range, default_value=slider_res_range[1], orientation='h', enable_events=True),
             ],
            [sg.Text('\ny resolution: ', size=(10, 2)),
             sg.pin(sg.Input(size=(5, 1), key='INPUT_Y', enable_events=True, expand_x=False, visible=True), vertical_alignment='b', ),
             # sg.Button('', key='ENTER_RES_Y', bind_return_key=True, visible=False),
             sg.Slider(size=(15, 16), key='SLIDER_Y', range=slider_res_range, default_value=slider_res_range[1], orientation='h', enable_events=True),
             ],
            [sg.Button('Resolution: + 1', key='BUTTON_RESOLUTION_INC_1')],
            [sg.Button('Resolution: + 5', key='BUTTON_RESOLUTION_INC_5')],
            [sg.Text('', key='FILLER_4', size=(2, 1), expand_y=False)],
            [sg.Text('\nNumber of colors: ', expand_x=True),
             sg.Slider(size=(15, 20), key='SLIDER_COLOR', range=slider_col_range, default_value=slider_col_range[1], orientation='h', enable_events=True),
             ],
            [sg.Button('Reset Image', key='RESET')]
        ])],
        [sg.Text('DEBUG INFO: ', visible=True, key='DEBUG_INFO'),
         sg.Text('Start with selecting image', expand_x=True, justification='left', visible=True, key='DEBUG')],
    ], size=size_control_column, pad=1, vertical_alignment='top', key='CCOL')

    color_col = sg.Column(layout=[
        [sg.Text('', key='COL_FILLER1', size=(1, 1), expand_y=False)],
        [sg.Text('Picked color: ', )],
        [sg.Text('', size=(1, 1)),
         sg.Image('', key='COLOR_IMAGE', size=size_color_image, background_color=background_color, visible=True, expand_y=False)],
        [sg.Text('RGB: ', key='COLOR_INFO_1', visible=True)],
        #[sg.Text('256, 000, 000', key='COLOR_RGB', expand_x=True, justification='left', visible=True)],
        [sg.Text('', key='COLOR_RGB', expand_x=True, justification='left', visible=True)],
        [sg.Text('HSV: ', key='COLOR_INFO_2', visible=True)],
        #[sg.Text('000, 100%, 100%', key='COLOR_HSV', expand_x=True, justification='left', visible=True)],
        [sg.Text('', key='COLOR_HSV', expand_x=True, justification='left', visible=True)],
    ], size=size_col_column, pad=1, vertical_alignment='top', key='COLOR_COL')

    main_image = sg.Image('', key='IMAGE', size=size_main_image, background_color=background_color, enable_events=True, visible=True, )

    layout = [[control_col, main_image, color_col]]

    window = sg.Window('Image Resizer', layout, size=size_window, finalize=True, resizable=False, element_justification='center', font=font)
    return window
