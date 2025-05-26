import base64
import copy

import numpy
import numpy as np
import io
from PIL import Image


def convert_bytes_to_image(decode_image: bytes):
    '''Функция для преобразования байтов в изображение'''
    return Image.open(io.BytesIO(base64.b64decode(decode_image)))


def convert_image_to_bytes(img):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    result_im_b64 = base64.b64encode(img_byte_arr).decode("utf8")

    result = result_im_b64.encode("utf-8")
    return result


def merge_tile(tile_upgrade, tile_added):
    '''
    Функция для объединения изображений плиток
    '''

    result_image = merge_image(convert_bytes_to_image(tile_upgrade.image),
                               convert_bytes_to_image(tile_added.image))
    tile = copy.copy(tile_upgrade)
    tile.image = convert_image_to_bytes(result_image)
    return tile


def merge_image(img1, img2):
    f_img_array = np.asarray(img1)
    s_img_array = np.asarray(img2)

    f_mask = np.logical_not((f_img_array[:, :, 3] != 255) | np.logical_and.reduce((f_img_array[:, :, 0] == 0,
                                                                                   f_img_array[:, :, 1] == 0,
                                                                                   f_img_array[:, :, 2] == 0,
                                                                                   f_img_array[:, :, 3] == 255)))
    s_mask = np.logical_not((s_img_array[:, :, 3] != 255) | np.logical_and.reduce((s_img_array[:, :, 0] == 0,
                                                                                   s_img_array[:, :, 1] == 0,
                                                                                   s_img_array[:, :, 2] == 0,
                                                                                   s_img_array[:, :, 3] == 255)))
    s_mask = f_mask ^ s_mask

    f_multiplied_array = f_img_array * f_mask[:, :, np.newaxis]
    s_multiplied_array = s_img_array * s_mask[:, :, np.newaxis]

    newImArray = f_multiplied_array + s_multiplied_array
    result = Image.fromarray(newImArray, "RGBA")
    return result


def clear_background(img):
    img_array = np.asarray(img)
    # newImArray = np.empty(img_array.shape, dtype='uint8')
    # mask = (img_array[:, :] == np.array([0, 0, 0, 255]))
    # mask = np.all(img_array == (0, 0, 0, 255), axis=0)
    mask = np.logical_and.reduce((img_array[:, :, 0] == 0,
                                  img_array[:, :, 1] == 0,
                                  img_array[:, :, 2] == 0,
                                  img_array[:, :, 3] == 255))
    newImArray = img_array.copy()
    newImArray[mask] = [0, 0, 0, 0]

    result = Image.fromarray(newImArray, "RGBA")
    return result
