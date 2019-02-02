# Resize all JPEG, GIF, PNG and BMP images inside a directory,
# recreating all directory tree into another path

import os
import math
import imghdr
from PIL import Image
from pathlib import Path

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output')
parser.add_argument('-s', '--side')
parser.add_argument('-m', '--megapixels')
args = parser.parse_args()

filetypes = ('jpeg', 'png', 'bmp', 'gif')

if (args.side is not None and float(args.side) > 0) or (args.megapixels is not None and float(args.megapixels) > 0):
    if args.input.__len__() and args.output.__len__():
        input_dir = str(args.input.rstrip('/'))
        output_dir = str(args.output.rstrip('/'))
        if args.side is not None:
            img_size_max = float(args.side)
        mp_max = 0
        if args.megapixels is not None:
            mp_max = float(args.megapixels)

        if args.verbose:
            print('Checking if output directory exists')
        if not os.path.exists(output_dir):
            if args.verbose:
                print('Creating directory: ' + input_dir)
            os.makedirs(output_dir)

        if os.path.exists(input_dir):
            pathlist = Path(input_dir).glob('**/*.*')
            count = {}
            total = 0
            try:
                for index, path in enumerate(pathlist):
                    filetype = imghdr.what(str(path))

                    if args.verbose:
                        print('Checking file type ' + filetype)
                    if filetype in filetypes:
                        path_in_str = str(path)
                        filename = str(path.name)

                        # I need to know the intermediate folders in order to create them before saving
                        relative_path = path_in_str[input_dir.__len__() + 1: -filename.__len__()]
                        absolute_output_path = str(Path(output_dir).joinpath(relative_path))

                        img = Image.open(path_in_str)
                        img_size_x, img_size_y = img.size
                        exif = img.info['exif']
                        if args.verbose:
                            print('Calculating new dimensions, original: [' + str(img_size_x) + 'x' + str(img_size_y) + ']')

                        if mp_max > 0:
                            coef = math.sqrt((img_size_x * img_size_y) / 1000000) / math.sqrt(mp_max)
                            h = int(img_size_x / coef)
                            v = int(img_size_y / coef)
                        else:
                            if img_size_x >= img_size_y:
                                h = int(img_size_max)
                                v = int(img_size_max * float(img_size_y) / float(img_size_x))
                            else:
                                v = int(img_size_max)
                                h = int(img_size_max * float(img_size_x) / float(img_size_y))

                        if args.verbose:
                            print('Resizing image ' + str(index + 1) + ' [' + str(h) + 'x' + str(v) + ']')
                        img = img.resize((int(h), int(v)), Image.ANTIALIAS)

                        if not os.path.exists(absolute_output_path):
                            os.makedirs(absolute_output_path)

                        img.save(str(Path(absolute_output_path).joinpath(filename)), exif=exif)

                        if filetype in count:
                            count[filetype] = count[filetype] + 1
                        else:
                            count[filetype] = 1

                        total = index + 1

                        if args.verbose:
                            print('Saved ' + filename)
            except KeyboardInterrupt:
                print('\n\nOh, no, a KeyboardInterrupt :(\nLet\'s see how was going on...')
                pass

            for item in count:
                print('Resized ' + str(count[item]) + ' ' + str(item) + ' images')
            print('Total: ' + str(total) + ' images')
        else:
            print('Invalid input directory, it cannot be opened')
    else:
        print('Invalid arguments, side must be an positive number')
else:
    print('Invalid arguments, side or megapixels must be present and positive numbers')
