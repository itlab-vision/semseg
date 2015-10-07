"""
Script leaves only unique and existing files from data subsets
"train_aug" and "trainval_aug" (eg val_aug)
"""

def readFileToSet(file_name, out):
	list_all_file = open(file_name, "rb")
	if (list_all_file == None):
		print "Failed to open a file."
		return 1

	for entry in list_all_file:
		out.add(entry[0:-1])

	list_all_file.close()

def printSetToFile(file_name, data):
	out = open(file_name, "wb+")
	for entry in data:
		out.write("%s %s\n" % ("/JPEGImages/" + entry + ".jpg", "/SegmentationAug/" + entry + ".png"))
	out.close()

if (__name__ == "__main__"):
	list_all = set()
	list_a = set()
	list_b = set()

	readFileToSet("list.txt", list_all)

	# TRAIN dataset
	readFileToSet("train.txt", list_a)
	readFileToSet("train_aug.txt", list_b)
	list_aug = (list_a | list_b) & list_all
	printSetToFile("train_aug_new.txt", list_aug)
	
	# TRAINVAL dataset
	readFileToSet("trainval.txt", list_a)
	readFileToSet("trainval_aug.txt", list_b)
	list_aug = (list_a | list_b) & list_all
	printSetToFile("trainval_aug_new.txt", list_aug)
