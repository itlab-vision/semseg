'''
Usage: python weak_markup_from_strong.py gt/dir output/dir
This tool enables easy creation of weak markup from strong one.

'''


from PIL import Image, ImageStat
import sys
import os



def show_help():
	print(__doc__)


class SegmentationResultsProcessor:
	classes = []
	results_directory = None
	gt_directory = None
	list_path = None


	def check_class_presence(self, image, class_index):
		assert(image.mode in ['1', 'L', 'P'])
		
		mask = image.point(lambda p: (p == class_index) * 255)
		mask = mask.convert('1')

		stat = ImageStat.Stat(gt)
		presence = (0 < stat.sum[0])

		return presence


	def process_image(self, image_path):
		classes_presence = [False] * len(self.classes) # (class presence, ...)
		
		image = Image.open(image_path)
		image = image.convert('P') # palette-based

		for class_index in range(len(self.classes)):
			classes_presence[class_index] = self.check_class_presence(image, class_index)

		return classes_presence


	def write_results(self, results_path, classes):
		results = open(results_path, 'w+')
		for class_index in range(1, len(self.classes)):
			if (classes[class_index] == False):
				continue
			
			results.write('%s' % (self.classes[class_index]))
			if (class_index < len(self.classes) - 1):
				results.write(os.linesep)


	def process(self):
		if (self.results_directory == None):
			raise Exception('Results directory is not set')
		if (self.gt_directory == None):
			raise Exception('Ground Truth directory is not set')

		for entry in os.listdir(gt_directory):
			entry = entry.strip()
			print('Processing entry \'%s\'' % (entry))

			gt_filepath = os.path.join(self.gt_directory, entry + os.extsep + 'png')
			result_filepath = os.path.join(self.results_directory, entry + os.extsep + 'txt')

			classes_presence = self.process_image(gt_filepath)
			self.write_results(result_filepath, classes_presence)


if (__name__ == '__main__'):
	if (len(sys.argv) != 3):
		show_help()
		exit()

	processor = SegmentationResultsProcessor()
	processor.gt_directory = os.path.abspath(sys.argv[1])
	processor.results_directory = os.path.abspath(sys.argv[2])
	processor.classes = [
		'background',
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