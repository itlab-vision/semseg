from PIL import Image
import sys
import os
"""
Usage: kitti_converter.py result/dir gt/dir images/list.txt
Converts KITTI gt to palette-based with conformance:
0 - background
1 - my lane
2 - other lanes
"""


def show_help():
    print(__doc__)


def class_conformance(p):
    if p == 76:
        return 0
    if p == 105:
        return 1
    if p == 0:
        return 2
    return 0


if (__name__ == "__main__"):
    if (len(sys.argv) != 4):
        show_help()
        exit()

    results_directory = os.path.abspath(sys.argv[1])
    gt_directory = os.path.abspath(sys.argv[2])
    list_path = os.path.abspath(sys.argv[3])

    images_list = open(list_path, 'r')

    for entry in images_list:
        entry = entry.strip()
        print('Processing entry \'%s\'' % (entry))

        result_filepath = os.path.join(results_directory, entry + os.extsep + 'png')
        gt_filepath = os.path.join(gt_directory, entry + os.extsep + 'png')

        image = Image.open(gt_filepath).convert("L").point(class_conformance)
        image.save(result_filepath)