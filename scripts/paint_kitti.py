from PIL import Image
import sys
import os
"""
Usage: paint_kitti.py input/dir output/dir
Converts grayscale inference to palette-based with conformance:
0 -> (0, 0, 0)
1 -> (255, 255, 0)
"""


def show_help():
    print(__doc__)


def class_conformance_r(p):
    if p == 0:
        return 0
    if p == 1:
        return 255
    return 0


def class_conformance_g(p):
    if p == 0:
        return 0
    if p == 1:
        return 255
    return 0


def class_conformance_b(p):
    if p == 0:
        return 0
    if p == 1:
        return 0
    return 0


if (__name__ == "__main__"):
    if (len(sys.argv) != 3):
        show_help()
        exit()

    input_directory = os.path.abspath(sys.argv[1])
    output_directory = os.path.abspath(sys.argv[2])

    for entry in os.listdir(input_directory):
        if (entry[-4:] != ".png"):
            continue

        print('Processing entry \'%s\'' % (entry))

        inference_filepath = os.path.join(input_directory, entry[:-4] + os.extsep + 'png')
        painted_inference_filepath = os.path.join(output_directory, entry[:-4] + os.extsep + 'png')

        image_channels = Image.open(inference_filepath).convert("P").split()
        painted_channels = list(3)
        painted_channels[0] = image_channels[0].point(class_conformance_r)
        painted_channels[1] = image_channels[1].point(class_conformance_g)
        painted_channels[2] = image_channels[2].point(class_conformance_b)
        Image.merge("RGB", painted_channels).save(painted_inference_filepath_filepath)