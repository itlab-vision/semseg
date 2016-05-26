from PIL import Image
import sys
import os
"""
Usage: kitti_converter.py gt/dir output/dir 
Converts KITTI gt to palette-based with conformance:
0 - background
1 - my lane
255 - something else
"""


def show_help():
    print(__doc__)


def class_conformance(p):
    if p == 76:
        return 0
    if p == 105:
        return 1
    if p == 0:
        return 255
    return 0


if (__name__ == "__main__"):
    if (len(sys.argv) != 3):
        show_help()
        exit()

    output_directory = os.path.abspath(sys.argv[1])
    gt_directory = os.path.abspath(sys.argv[2])

    for entry in os.listdir(gt_directory):
        print('Processing entry \'%s\'' % (entry))

        gt_filepath = os.path.join(gt_directory, entry + os.extsep + 'png')
        result_filepath = os.path.join(output_directory, entry + os.extsep + 'png')

        image = Image.open(gt_filepath).convert("L").point(class_conformance)
        image.save(result_filepath)