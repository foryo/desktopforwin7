import json
import os
import time

import win32api
import win32con
from urllib import request

import win32gui

from PIL import Image


def get_image_dict():
    url = "http://cn.bing.com/HPImageArchive.aspx?format=js&idx=-1&n=8"
    response = request.urlopen(url)
    ijson = json.loads(response.read().decode("utf-8"))
    images = ijson["images"]
    dict = {}
    for image in images:
        dict[image["copyright"].replace("/", " ")] = image["url"]
    return dict


def set_wallpaper(src_path):
    reg_key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_ALL_ACCESS)
    current_path = win32api.RegQueryValueEx(reg_key, "Wallpaper")[0]
    if current_path != src_path:
        print("---------set wallpaper：{}-------".format(src_path))
        win32api.RegSetValueEx(reg_key, "WallPaper", 0, win32con.REG_SZ, src_path)
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, src_path, 1 + 2)


def set_watermark(text, image):
    from PIL import ImageDraw, ImageFont
    font = ImageFont.truetype('simsun.ttc', 15)
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), text, font=font)


def save_image(dict):
    files_path = []
    target_folder = os.getcwd() + "\\" +"picture";
    if os.path.isdir(target_folder) == False :
        os.mkdir(target_folder);
    for key in dict.keys():
        file_path = target_folder + "\\" + key.replace("/", " ") + ".bmp"
        if os.path.exists(file_path):
            files_path.append(file_path)
            continue
        image = Image.open(request.urlopen(dict[key]))
        set_watermark(key,image)
        image.save(file_path)
        print("---------save image：{}---------".format(file_path))
        files_path.append(file_path)
    return files_path


def loop_set_wallpaper(files_path):
    index = 0
    while (True):
        set_wallpaper(files_path[index % len(files_path)])
        index = index + 1
        time.sleep(60 * 1)


def main():
    dict = get_image_dict()
    files_path = save_image(dict)
    loop_set_wallpaper(files_path)


if __name__ == '__main__':
    main()
