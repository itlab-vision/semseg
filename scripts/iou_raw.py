"""
Usage: python segmentation_accuracy.py segmentation/dir gt/dir images_list.txt

This tool calculates a IoU score for set of given images
using a formula: intersection / union.
"""


from PIL import Image, ImageStat
import sys
import os



def show_help():
    print(__doc__)


class SegmentationResultsProcessor:
    """
    For customizing a set of existing classes specify 
    classes field.

    results directory - a full path to results folder
    gt directory - a full path to ground truth folder
    list path - a full path to images list (without extensions)
    """

    classes = []
    results_directory = None
    gt_directory = None
    list_path = None


    def calculate_image_IoU(self, image, gt, class_index):
        """
        Returns an image intersection and union scores
        """

        assert(image.mode == 'P')
        assert(gt.mode == 'P')
        
        image_mask = image.point(lambda p: (p == class_index) * 255)
        gt_mask = gt.point(lambda p: (p == class_index) * 255)
        gt_mask = gt_mask.convert('1')

        intersection = Image.new('1', image.size, 0)
        intersection.paste(image_mask, gt_mask)

        stat = ImageStat.Stat(intersection)
        intersection_count = stat.sum[0] / 255

        unknown_label_mask = gt.point(lambda p: (p < 255) * 255)
        unknown_label_mask = unknown_label_mask.convert('1')
        stat = ImageStat.Stat(image_mask, unknown_label_mask)
        image_count = stat.sum[0] / 255

        stat = ImageStat.Stat(gt_mask)
        gt_count = stat.sum[0] / 255

        union_count = image_count + gt_count - intersection_count

        presence = (gt_count != 0)

        return (intersection_count, union_count, presence)


    def check_segmentation(self, image):
        """
        Assures that image segmentation is correct
        Throws an exception on failure
        """

        assert(image.mode in ['1', 'L', 'P'])
        image_mask = image.point(lambda p: (len(self.classes) <= p) and (p < 255))
        stat = ImageStat.Stat(image_mask)

        if (0 < stat.sum[0]):
            raise Exception('Image has an unexpected class index')


    def process_image(self, image_path, gt_path):
        """
        Throws an exception if images are not comparable
        """

        IoUs = [(0, 0, 0)] * len(self.classes) # (intersection, union, class presence)
        
        image = Image.open(image_path)
        image = image.convert('P')
        self.check_segmentation(image)

        gt = Image.open(gt_path)
        gt = gt.convert('P')
        self.check_segmentation(gt)

        if (image.width != gt.width or image.height != gt.height):
            raise Exception("Image sizes are different")

        for class_index in range(len(self.classes)):
            IoUs[class_index] = self.calculate_image_IoU(image, gt, class_index)

        return IoUs


    def process(self):
        """
        Processes the given set of images and returns an IoU score.
        Throws an exception on wrong input parameters
        """

        if (self.results_directory == None):
            raise Exception('Segmentation directory is not set')
        if (self.gt_directory == None):
            raise Exception('Ground Truth directory is not set')
        if (self.list_path == None):
            raise Exception('Images list path is not set')

        classes_metrics = [ [0, 0] for i in range(len(self.classes)) ] # (intersection, union) per class

        images_list = open(self.list_path, 'r')

        for entry in images_list:
            entry = entry.strip()
            print('Processing entry \'%s\'' % (entry))

            result_filepath = os.path.join(self.results_directory, entry + os.extsep + 'png')
            gt_filepath = os.path.join(self.gt_directory, entry + os.extsep + 'png')

            current_metrics = self.process_image(result_filepath, gt_filepath)
            for i in range(len(self.classes)):
                classes_metrics[i][0] += current_metrics[i][0]
                classes_metrics[i][1] += current_metrics[i][1]

        classes_IoU = [0.0] * len(self.classes)
        for i in range(len(self.classes)):
            if (0 < classes_metrics[i][1]):
                classes_IoU[i] = classes_metrics[i][0] / classes_metrics[i][1]

        overall_classes_presented = 0
        overall_accuracy = 0.0
        for i in range(1, len(self.classes)):
            overall_classes_presented += (0 < classes_metrics[i][1])
            overall_accuracy += classes_IoU[i]

        if (0 < overall_classes_presented):
            overall_accuracy /= overall_classes_presented

        self.classes_metrics = classes_IoU
        self.overall_accuracy = overall_accuracy


    def show_results(self):
        print('Segmentation accuracy (IoU metric)')
        print('Overall accuracy: %6.3f%%' % (100.0 * self.overall_accuracy))
        print('Per class accuracy:')
        for i in range(len(self.classes)):
            print('  %14s: %6.3f%%' % \
                (self.classes[i] , 100.0 * self.classes_metrics[i]) )


if (__name__ == '__main__'):
    if (len(sys.argv) != 4):
        show_help()
        exit()

    processor = SegmentationResultsProcessor()
    processor.results_directory = os.path.abspath(sys.argv[1])
    processor.gt_directory = os.path.abspath(sys.argv[2])
    processor.list_path = os.path.abspath(sys.argv[3])
    processor.classes = [
        'background', # keep first
        'aeroplane',
        'bicycle',
        'bird',
        'boat',
        'bottle',
        'bus',
        'car',
        'cat',
        'chair',
        'cow',
        'diningtable',
        'dog',
        'horse',
        'motorbike',
        'person',
        'pottedplant',
        'sheep',
        'sofa',
        'train',
        'tvmonitor'
    ]
    processor.process()
    processor.show_results()