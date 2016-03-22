'''
Usage: python segmentation_accuracy.py segmentation/dir gt/dir images_list.txt
'''


from PIL import Image, ImageStat
import sys
import os
import numpy



def show_help():
	print(__doc__)


class SegmentationResultsProcessor:
	Classes = [
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

	results_directory = None
	gt_directory = None
	list_path = None

	def check_segmentation(self, image):
		assert(image.mode in ['1', 'L', 'P'])
		image_mask = image.point(lambda p: (len(self.Classes) <= p) and (p < 255))

		stat = ImageStat.Stat(image_mask)
		if (0 < stat.sum[0]):
			raise Exception('Image has an unexpected class index')


	def process(self):
		if (self.results_directory == None):
			raise Exception('Segmentation directory is not set')
		if (self.gt_directory == None):
			raise Exception('Ground Truth directory is not set')
		if (self.list_path == None):
			raise Exception('Images list path is not set')

		images_list = open(self.list_path, 'r')
		confcounts = numpy.zeros((len(self.Classes), len(self.Classes)))

		for entry in images_list:
			entry = entry.strip()
			print('Processing entry \'%s\'' % (entry))

			result_filepath = os.path.join(self.results_directory, entry + os.extsep + 'png')
			gt_filepath = os.path.join(self.gt_directory, entry + os.extsep + 'png')

			# load groudtruth image
			gtim = numpy.asarray(Image.open(gt_filepath).convert('L')).astype(float)
			# load segmentation image
			resim = numpy.asarray(Image.open(result_filepath).convert('L')).astype(float)
			
			if (resim.shape[0] != resim.shape[0] or resim.shape[1] != resim.shape[1]):
				raise Exception("Image sizes are different") 

			# sumim = 1 + gtim + resim * num;
			sumim = 1 + gtim + resim * len(self.Classes)			
			# locs = gtim < 255
			locs = gtim < 255
			# hs = histc(sumim(locs), 1 : num * num);
			maskedsumim = numpy.extract(locs, sumim)
			[hs, bin_edges] = numpy.histogram(maskedsumim, bins = range(1, len(self.Classes) * len(self.Classes) + 2))
			# confcounts(:) = confcounts(:) + hs(:);
			confcounts += numpy.reshape(hs, (len(self.Classes), len(self.Classes)))

		# conf = 100*confcounts./repmat(1E-20 + sum(confcounts,2), [1 size(confcounts,2)]);
		conf = 100 * numpy.divide(confcounts, numpy.repeat(
                    numpy.sum(confcounts, axis = 1)[:, numpy.newaxis], len(self.Classes), 1) + 1E-20)
		# overall_acc = 100*sum(diag(confcounts)) / sum(confcounts(:));
		self.overall_accuracy = 100 * numpy.sum(numpy.diagonal(confcounts)) / numpy.sum(confcounts)
		
		

	def show_results(self):
		print('Segmentation accuracy (IoU metric)')
		print('Overall accuracy: %6.3f%%' % self.overall_accuracy)


if (__name__ == '__main__'):
	if (len(sys.argv) <= 1):
		show_help()
		exit()

	processor = SegmentationResultsProcessor()
	processor.results_directory = os.path.abspath(sys.argv[1])
	processor.gt_directory = os.path.abspath(sys.argv[2])
	processor.list_path = os.path.abspath(sys.argv[3])
	processor.process()
	processor.show_results()
