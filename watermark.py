'''
DESCRIPTION:
   Watermark image files.

'''

import argparse
import os
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

class Error(Exception):
    pass


IMAGE_EXTENSTIONS = ('.png', '.jpg', '.jpeg' )

def process_command_line(argv):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description= __doc__ )
    return parser.prog, parser.parse_args(argv)


def process_file( file_path, dir_out):
    print(f'process file: {file_path.name}')

    original_image = Image.open(file_path)
    draw = ImageDraw.Draw(original_image)
    text = 'property of Todd MacCulloch'
    font = ImageFont.truetype('Comic Sans MS.ttf', 24)
    
    textwidth, textheight = draw.textsize(text, font)
    width, height = original_image.size 
    x = width/2 - textwidth/2
    y = height - textheight - 100

    # Applying text on image via draw object
    draw.text((x, y), text, font=font) 

    path_out = dir_out / file_path.name
    print(f'file out: {path_out }' )

    original_image.save( path_out )

   

def process_directory(fdir):
    print(f'processing: {fdir}')
    path_in = pathlib.Path(fdir)
    path_in.resolve()
    assert( path_in.is_dir )

    stem_out = f'{path_in.stem}-wm' 
    path_out = pathlib.Path(path_in.parents[0]) / stem_out
    print(f'path_out: {path_out}')
    if not path_out.exists():
        path_out.mkdir()
    assert( path_out.is_dir )

    for cur_path in path_in.iterdir():
        if cur_path.is_file and cur_path.suffix in IMAGE_EXTENSTIONS:
            process_file(cur_path, path_out)
    

def main(argv=None):
    try:
        program_name, args = process_command_line(argv)
        print(f'{program_name} start')
        print(f'current directory: {os.getcwd()}')

        image_dir = 'images'
        process_directory(os.path.join(os.getcwd(), image_dir))

        print(f'{program_name} end')
    except Error as err:
        print(f'\nERROR:\n{err}\n')


if __name__ == '__main__' :
    sys.exit(main())