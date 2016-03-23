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
			
			if (resim.shape[0] != gtim.shape[0] or resim.shape[1] != gtim.shape[1]):
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

                # class accuracy
		self.class_acc = numpy.zeros(len(self.Classes))
		denoms = numpy.sum(confcounts, axis = 0)
		for i in range(0, len(self.Classes)):
                        # denom = sum(confcounts(i, :)) в denoms
                        if (denoms[i] == 0):
                                denoms[i] = 1
                        # class_acc(i) = 100 * confcounts(i, i) / denom;
                        self.class_acc[i] = 100 * confcounts[i][i] / denoms[i]
		self.aver_class_acc = numpy.sum(self.class_acc) / len(self.Classes)

		# pixel IoU
		self.accuracies = numpy.zeros(len(self.Classes))
		gtj = numpy.sum(confcounts, axis = 1)
		resj = numpy.sum(confcounts, axis = 0)
		for j in range(0, len(self.Classes)):
                        # gtj=sum(confcounts(j,:)) в gtj
                        # resj=sum(confcounts(:,j)) в resj
                        # gtjresj=confcounts(j,j);
                        gtjresj = confcounts[j][j]
                        # denom = (gtj+resj-gtjresj);
                        denom = gtj[j] + resj[j] - gtjresj
                        if (denom == 0):
                                denom = 1
                        # accuracies(j)=100*gtjresj/denom;
                        self.accuracies[j] = 100 * gtjresj / denom
		self.aver_accuracy = numpy.sum(self.accuracies) / len(self.Classes)
		

	def show_results(self):		
		print('----------------------------------')
		print('Percentage of pixels correctly labelled overall: %6.3f%%' % self.overall_accuracy)
		print('----------------------------------')
		print('Mean Class Accuracy:: %6.3f%%' % self.aver_class_acc)
		print('Per class accuracy:')
		for i in range(len(self.Classes)):
			print('  %14s: %6.3f%%' % \
				(self.Classes[i] , self.class_acc[i]) )
		print('----------------------------------')
		print('Average accuracy: %6.3f%%' % self.aver_accuracy)
		print('Accuracy for each class (intersection/union measure)')
		for i in range(len(self.Classes)):
			print('  %14s: %6.3f%%' % \
				(self.Classes[i] , self.accuracies[i]) )
		print('----------------------------------')


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
