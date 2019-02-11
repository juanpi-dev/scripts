#!/usr/bin/env python
# Move videos from downloaded TV series to structured directories by season

import os
import re
import shutil
from pathlib import Path

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-I', '--info', action='store_true')
parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output')
parser.add_argument('-s', '--simulate', action='store_true')
args = parser.parse_args()

extensions = ('mkv', 'avi', 'mp4')

if args.input is not None and args.output is not None:
    if args.input.__len__() and args.output.__len__():
        input_dir = str(args.input.rstrip('/'))
        output_dir = str(args.output.rstrip('/'))
        #
        # if args.verbose:
        #     print('Checking if output directory exists')
        # if not os.path.exists(output_dir):
        #     if args.verbose:
        #         print('Creating directory: ' + input_dir)
        #     os.makedirs(output_dir)

        if os.path.exists(input_dir):
            pathlist = Path(input_dir).glob('**/*.*')
            count = {}
            total = 0
            try:
                for index, path in enumerate(pathlist):
                    extension = os.path.splitext(str(path))[1][1:]
                    # if args.verbose:
                    #     print('Checking file extension ' + extension)
                    if extension.lower() in extensions:
                        filename = os.path.basename(str(path))
                        # m = re.search('(.+)(?:s([0-9]{2,})e([0-9]{2,})|([0-9]+)([0-9]{2,})|([0-9]+)x([0-9]{2,})).*/i', filename)
                        # m = re.search('(.+).*s([0-9]+)e([0-9])+.*', filename)
                        m = re.search('(.+)[sS]([0-9]{2,})[eE]([0-9]{2,}).*', filename)

                        if m is not None:
                            if args.verbose:
                                print('\nProcessing ' + filename)

                            final_filename = re.sub(
                                r'[^\x20\x30-\x39\x41-\x5A\x61-\x7A]+', ' ', str(m.group(1))
                            ).strip().lower()
                            # print('Title: ' + final_filename
                            #       + ', season: ' + str(m.group(2))
                            #       + ', episode: ' + str(m.group(3)))

                            season_number = 0
                            episode_number = 0

                            if m.group(2) is not None:
                                season_number = m.group(2)
                                episode_number = str(int(m.group(3)))
                            # if m.group(4) is not None:
                            #     season_number = m.group(4)
                            #     episode_number = str(int(m.group(5)))
                            # if m.group(6) is not None:
                            #     season_number = m.group(6)
                            #     episode_number = str(int(m.group(7)))

                            season_number = str(int(season_number))
                            episode_number = str(int(episode_number))
                            target_dir = os.path.join(str(output_dir), final_filename)
                            target_dir = os.path.join(str(target_dir), 'season ' + season_number)

                            if args.verbose:
                                print('Season: ' + season_number + ', episode: ' + episode_number)

                            if not os.path.exists(target_dir):
                                if args.verbose:
                                    print('Creating directory: ' + target_dir)
                                if not args.simulate:
                                    os.makedirs(target_dir)
                            else:
                                if args.verbose:
                                    print('It\'s ok, directory "' + target_dir + '" already exists')

                            if args.verbose:
                                print('Moving ' + filename)
                            if not args.simulate:
                                shutil.move(str(path), str(target_dir))

                            total = total + 1

                            if args.verbose:
                                print('Saved ' + filename)
            except KeyboardInterrupt:
                print('\n\nOh, no, a KeyboardInterrupt :(\nLet\'s see how was going on...')
                pass
            print('Total: ' + str(total) + ' processed files')
        else:
            print('Invalid input directory, it cannot be opened')
    else:
        print('Invalid arguments, input and output must be set')
else:
    print('Invalid arguments, input and output must be set')
