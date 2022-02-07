import os
from pathlib import Path
from cairosvg import svg2png


def svg_to_png(src, dest, width, height):
    print("Converting {0} into {1}".format(src, dest))
    svg2png(url=src
            , write_to=dest
            , parent_width=width
            , parent_height=height)


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

                    dest_png = str(png_path)+'\\'+svg
                    dest_png = dest_png.replace('.svg', '.png')

                    svg_to_png(src=src_svg, dest=dest_png, width=width, height=height)
