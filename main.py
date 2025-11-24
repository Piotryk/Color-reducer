import base64
from PIL import Image
import io
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import FigureCanvasAgg
import PySimpleGUI as sg
import matplotlib
import window

'''
fig, ax = plt.subplots(figsize=(5, 4))
fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
#img = np.asarray(Image.open('a1.jpg'))
t = np.arange(0, 3, .01)
img = Image.open('a1.jpg')
img = img.resize(size_main_image)
img.save('a1.png', format='png')
fig.add_subplot(111).imshow(img)
#fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))


img = PIL.Image.new('RGB', (100, 100), (255, 255, 255))
img.thumbnail((1, 1), PIL.Image.LANCZOS)
bio = io.BytesIO()
img.save(bio, format='PNG')
imgbytes = bio.getvalue()
window[key].update(image_data=imgbytes)

'''
def im():
    fig, ax = plt.subplots(figsize=(6 / 2.51, 6 / 2.51))
    img = Image.open('a1.jpg')
    ax.imshow(img)
    img.thumbnail((64, 64))  # resizes image in-place
    plt.show()


def debug(main_window, text):
    main_window['DEBUG'].update(text)
    main_window.refresh()


def draw_figure(image_element, img):
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    imgbytes = buf.getvalue()
    image_element.update(data=imgbytes, size=(512, 512))



def draw_figure_plt(image_element, fig):
    plt.close('all')  # erases previously drawn plots
    canv = FigureCanvasAgg(fig)
    buf = io.BytesIO()
    canv.print_figure(buf, format='png')
    if buf is not None:
        buf.seek(0)
        image_element.update(buf.read())


def make_plt_image(filepath):
    resolution = (256, 256)
    px = 1 / plt.rcParams['figure.dpi']
    plt.tight_layout(pad=0)

    fig = plt.figure(figsize=(512*px, 512*px))
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    #ax.set_axis_off()
    fig.add_axes(ax)

    img = Image.open(filepath).resize(resolution)
    resolution = img.size
    print(resolution)
    ax.imshow(img, interpolation='none')  # v2: i=nearest
    ax.set_xticks(np.arange(0, resolution[0] - 1, 1))
    ax.set_yticks(np.arange(0, resolution[1] - 1, 1))

    # Labels for major ticks
    ax.set_xticklabels(np.arange(1, resolution[0], 1))
    ax.set_yticklabels(np.arange(1, resolution[1], 1))

    # Minor ticks
    ax.set_xticks(np.arange(-.5, resolution[0], 1), minor=True)
    ax.set_yticks(np.arange(-.5, resolution[1], 1), minor=True)

    # Gridlines based on minor ticks
    ax.grid(which='minor', color='w', linestyle='-', linewidth=0)

    # Remove minor ticks
    ax.tick_params(which='minor', bottom=False, left=False)
    print(ax.bbox)
    # bbox_inches='tight', pad_inches=0.0
    return fig


def resize(main_window, original_image, target_res):
    if original_image in None:
        return None
    o_size = original_image.size
    if o_size[0] > 512 or o_size[1] > 512:
        factor = max(img.size[0], img.size[1]) / 512
        size = (int(img.size[0] / c), int(img.size[1] / c))
    pass


def main(mode):
    original_image = None
    ratio = 1
    flag_resized = False
    flag_recolored = False

    main_window = window.make_window(mode)

    # MAIN LOOP
    while True:
        event, values = main_window.read()
        print(event, values)
        relative_mouse_location = (main_window.mouse_location()[0] - main_window.CurrentLocation()[0], main_window.mouse_location()[1] - main_window.CurrentLocation()[1])
        print(relative_mouse_location)
        relative_image_pos = (385, 50)

        if event == sg.WIN_CLOSED:
            main_window.close()
            break

        if event == 'SELECT':
            image_path = values['SELECT']
            original_image = Image.open(image_path)#.resize(size_main_image)
            original_size = real_size = original_image.size

            current_img = original_image

            if original_size[0] > 512 or original_size[1] > 512:
                ratio = max(original_size[0], original_size[1]) / 512
                real_size = (int(original_size[0] / ratio), int(original_size[1] / ratio))
                current_img = original_image.resize(real_size, resample=Image.Resampling.BILINEAR)

            draw_figure(main_window['IMAGE'], current_img)
            main_window['INFO_ORIGINAL_RES'].update(f'{original_size[0]} x {original_size[1]}')

        # todo: note
        if original_image is None:
            continue

        if event == 'BUTTON_RESOLUTION_INC_1':
            current_res = (int(values['SLIDER_X']) + 1, int(values['SLIDER_Y']) + 1)
            main_window['SLIDER_X'].update(int(values['SLIDER_X']) + 1)
            main_window['SLIDER_Y'].update(int(values['SLIDER_Y']) + 1)

            img = original_image
            if flag_recolored:
                img = img.convert('P', palette=Image.ADAPTIVE, colors=int(values['SLIDER_COLOR']))

            imgSmall = img.resize(current_res, resample=Image.Resampling.BILINEAR)
            img = imgSmall.resize(real_size, Image.Resampling.NEAREST)

            draw_figure(main_window['IMAGE'], img)
            debug(main_window, f'resized image to {current_res}')
            flag_resized = True

        if event == 'BUTTON_RESOLUTION_INC_5':
            inc = 5
            current_res = (int(values['SLIDER_X']) + inc, int(values['SLIDER_Y']) + inc)
            main_window['SLIDER_X'].update(int(values['SLIDER_X']) + inc)
            main_window['SLIDER_Y'].update(int(values['SLIDER_Y']) + inc)

            img = original_image
            if flag_recolored:
                img = img.convert('P', palette=Image.ADAPTIVE, colors=int(values['SLIDER_COLOR']))

            imgSmall = img.resize(current_res, resample=Image.Resampling.BILINEAR)
            img = imgSmall.resize(real_size, Image.Resampling.NEAREST)

            draw_figure(main_window['IMAGE'], img)
            debug(main_window, f'resized image to {current_res}')
            flag_resized = True

        if event == 'SLIDER_X':
            if values['BUTTON_RATIO']:
                y_res = values['SLIDER_X'] / original_size[0] * original_size[1]

                main_window['SLIDER_Y'].update(int(y_res))
                current_res = (int(values['SLIDER_X']), int(y_res))
            else:
                current_res = (int(values['SLIDER_X']), int(values['SLIDER_Y']))

            img = original_image
            if flag_recolored:
                img = img.convert('P', palette=Image.ADAPTIVE, colors=int(values['SLIDER_COLOR']))

            imgSmall = img.resize(current_res, resample=Image.Resampling.BILINEAR)
            img = imgSmall.resize(real_size, Image.Resampling.NEAREST)

            draw_figure(main_window['IMAGE'], img)
            debug(main_window, f'resized image to {current_res}')
            flag_resized = True

        if event == 'SLIDER_Y':
            if values['BUTTON_RATIO']:
                x_res = values['SLIDER_Y'] / original_size[1] * original_size[0]

                main_window['SLIDER_X'].update(int(x_res))
                current_res = (int(x_res), int(values['SLIDER_Y']))
            else:
                current_res = (int(values['SLIDER_X']), int(values['SLIDER_Y']))

            imgSmall = original_image.resize(current_res, resample=Image.Resampling.NEAREST)  #or BILINEAR?
            img = imgSmall.resize(real_size, Image.Resampling.NEAREST)

            if flag_recolored:
                img = img.convert('P', palette=Image.ADAPTIVE, colors=int(values['SLIDER_COLOR']))

            draw_figure(main_window['IMAGE'], img)
            debug(main_window, f'resized image to {current_res}')
            flag_resized = True

        if event == 'SLIDER_COLOR':
            img = original_image

            if flag_resized:
                current_res = (int(values['SLIDER_X']), int(values['SLIDER_Y']))  # będzie ok bo
                imgSmall = original_image.resize(current_res, resample=Image.Resampling.NEAREST)  # or BILINEAR?
                img = imgSmall.resize(real_size, Image.Resampling.NEAREST)
            else:
                if original_size[0] > 512 or original_size[1] > 512:
                    ratio = max(original_size[0], original_size[1]) / 512
                    real_size = (int(original_size[0] / ratio), int(original_size[1] / ratio))
                    img = original_image.resize(real_size, resample=Image.Resampling.BILINEAR)

            img = img.convert('P', palette=Image.ADAPTIVE, colors=int(values['SLIDER_COLOR']))
            draw_figure(main_window['IMAGE'], img)
            debug(main_window, f'Reduced number of colors')
            flag_recolored = True

        if event == "RESET":
            if original_size[0] > 512 or original_size[1] > 512:
                ratio = max(original_size[0], original_size[1]) / 512
                real_size = (int(original_size[0] / ratio), int(original_size[1] / ratio))
                current_img = original_image.resize(real_size, resample=Image.Resampling.BILINEAR)
            draw_figure(main_window['IMAGE'], current_img)
            flag_resized = False
            flag_recolored = False

        if event == 'ENTER_RES':
            if values['INPUT_X'] and values['INPUT_Y']:
                main_window['SLIDER_X'].update(int(values['INPUT_X']))
                main_window['SLIDER_Y'].update(int(values['INPUT_Y']))
            elif values['INPUT_X'] and values['BUTTON_RATIO'] and not values['INPUT_Y']:
                    y_res = values['SLIDER_X'] / original_size[0] * original_size[1]
                    main_window['SLIDER_Y'].update(int(y_res))
            elif values['INPUT_Y'] and values['BUTTON_RATIO'] and not values['INPUT_X']:
                x_res = values['SLIDER_Y'] / original_size[1] * original_size[0]
                main_window['SLIDER_X'].update(int(x_res))
            else:
                continue

            current_res = (int(values['SLIDER_X']), int(values['SLIDER_Y']))
            imgSmall = original_image.resize(current_res, resample=Image.Resampling.NEAREST)  # or BILINEAR?
            img = imgSmall.resize(real_size, Image.Resampling.NEAREST)

            if flag_recolored:
                img = img.convert('RGB', palette=Image.ADAPTIVE, resample=Image.Resampling.NEAREST, colors=int(values['SLIDER_COLOR']))
            draw_figure(main_window['IMAGE'], img)
            debug(main_window, f'resized image to {current_res}')
            flag_resized = True

        if event == 'IMAGE':
            current_res = real_size
            if flag_resized:
                current_res = (int(values['SLIDER_X']), int(values['SLIDER_Y']))

            # get pixel
            #if not current_res[0] == current_res[1]:
            offset_px = (512 - min(current_res[0], current_res[1]) / max(current_res[0], current_res[1])) / 2
            offset_px = 256 * (1 - min(current_res[0], current_res[1]) / max(current_res[0], current_res[1]))

            if not flag_recolored and not flag_resized:
                img = original_image

            if current_res[0] > current_res[1]:
                offset = (0, offset_px)
            else:
                offset = (offset_px, 0)

            inside_mouse_location = (relative_mouse_location[0] - relative_image_pos[0] - offset[0], relative_mouse_location[1] - relative_image_pos[1] - offset[1])

            pixel_no = (int(inside_mouse_location[0] / 1024 * current_res[0]), int(inside_mouse_location[1] / 1024 * current_res[1]))

            color_rgb = img.resize(current_res, resample=Image.Resampling.NEAREST).convert('RGB').getpixel(pixel_no)
            color_hsv = img.resize(current_res, resample=Image.Resampling.NEAREST).convert('RGB').convert('HSV').getpixel(pixel_no)
            print(pixel_no, color_rgb, img.size)
            #main_window['COLOR_RGB'].update(str(color_rgb))
            #main_window['COLOR_HSV'].update(str(color_hsv))



if __name__ == '__main__':
    mode = '4k'   # otherwise 4k mode
    main(mode)
