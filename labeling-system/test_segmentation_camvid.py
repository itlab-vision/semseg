import numpy as np
import cv2
import argparse
import glob
caffe_root = 'PATH_TO_SEGNET!!! LINE 5'
import sys
sys.path.insert(0, caffe_root + 'python')

import caffe

# Import arguments
parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, required=True)
parser.add_argument('--weights', type=str, required=True)
parser.add_argument('--path_to_images', type=str, required=True)
parser.add_argument('--iter', type=int, required=True)
parser.add_argument('--result_dir', type=str, required=True)
args = parser.parse_args()

caffe.set_mode_gpu()

net = caffe.Net(args.model,
                args.weights,
                caffe.TEST)

images = [caffe.io.load_image(im_f)
                 for im_f in glob.glob(args.path_to_images + '/*.png')]

for i in range(0, args.iter):

    input = images[i]
    inp = np.array([input[:,:,0], input[:,:,1], input[:,:,2]])
    net.blobs['data'] = inp
    net.forward()

    image = images[i]
   	#label = net.blobs['label'].data
    predicted = net.blobs['prob'].data
    #image = np.squeeze(image[0,:,:,:])
    output = np.squeeze(predicted[0,:,:,:])
    ind = np.argmax(output, axis=0)

    r = ind.copy()
    g = ind.copy()
    b = ind.copy()

    Sky = [128,128,128]
    Building = [128,0,0]
    Pole = [192,192,128]
    Road_marking = [255,69,0]
    Road = [128,64,128]
    Pavement = [60,40,222]
    Tree = [128,128,0]
    SignSymbol = [192,128,128]
    Fence = [64,64,128]
    Car = [64,0,128]
    Pedestrian = [64,64,0]
    Bicyclist = [0,128,192]
    Unlabelled = [0,0,0]

    label_colours = np.array([Sky, Building, Pole, Road, Pavement, Tree, SignSymbol, Fence, Car, Pedestrian, Bicyclist, Unlabelled])
    for l in range(0,12):
    	r[ind==l] = label_colours[l,0]
    	g[ind==l] = label_colours[l,1]
    	b[ind==l] = label_colours[l,2]

	rgb = np.zeros((ind.shape[0], ind.shape[1], 3))
	rgb[:,:,0] = r
	rgb[:,:,1] = g
	rgb[:,:,2] = b

	cv2.imwrite(args.result_dir + ('/segnet_{}.png').format(i), rgb)

print 'Success!'

