import os
from pathlib import Path
from cairosvg import svg2png
import xml.etree.ElementTree as ET
import numpy as np
import cv2


def svg_to_png(src, dest, width, height):
    print("Converting {0} into {1}".format(src, dest))
    svg2png(url=src
            , write_to=dest
            , parent_width=width
            , parent_height=height)


def remove_back_svg(svg_path):
    ET.register_namespace('', "http://www.w3.org/2000/svg")  # should add namespace
    tree = ET.parse(svg_path)
    root = tree.getroot()

    for first_level in list(root):
        for second_level in list(first_level):
            items = second_level.items()[0]
            tag_name = items[1]
            if "B" in tag_name:
                first_level.remove(second_level)

    tree.write(svg_path)


def resize_svg(svg_path):
    ET.register_namespace('', "http://www.w3.org/2000/svg")  # should add namespace
    tree = ET.parse(svg_path)
    root = tree.getroot()

    size = root.attrib['viewBox']
    size = size.split(' ')

    height = float(size[2]) / 2

    size = size[0] + " " + size[1] + " " + str(height) + " " + size[3]

    root.attrib['viewBox'] = size

    tree.write(svg_path)


def resize_png(png_path):

    img = cv2.imread(png_path, cv2.IMREAD_UNCHANGED)

    bw_img = (img[:, :, 3] > 0)  # alhpa != 0

    img_width = bw_img.shape[1]

    last_point = 0
    current_w = 0

    points = []

    first = True

    while current_w < img_width:
        row_arr = bw_img[current_w, :]
        positive_indices = np.where(row_arr)  # for each column of pixels

        if (current_w - last_point) > 1:
            break

        if len(positive_indices[0]) == 0:  # if there is no meaningful pixel, continue
            current_w += 1
            if len(points) == 0:
                last_point = current_w
            continue

        if first:
            first = False
            points.append(current_w)

        # for every width_stride column
        current_w += 1
        last_point = current_w

    points.append(last_point)
    
    print(points)


if __name__ == '__main__':
    DATA_ROOT = 'D:/sketch-pattern_dataset/sketch'

    png_path = Path(DATA_ROOT, '_PNG_FOLDER_')
    png_path.mkdir(parents=True, exist_ok=True)

    width = 512  # user input (default = 512)
    height = 512  # user input (default = 512)

    root_path = Path(DATA_ROOT)

    dir_list = [i for i in root_path.glob('*')]

    for dir in dir_list:
        p = Path(dir)
        for sub_dir in p.glob('*'):
            if str(sub_dir) == str(dir) + '\\l0':
                file = os.listdir(str(sub_dir))
                for svg in file:
                    src_svg = str(sub_dir)+'\\'+svg

                    remove_back_svg(src_svg)

                    dest_png = str(png_path)+'\\'+svg
                    dest_png = dest_png.replace('.svg', '.png')

                    resize_svg(src_svg)
                    svg_to_png(src=src_svg, dest=dest_png, width=width, height=height)
                    resize_png(dest_png)

