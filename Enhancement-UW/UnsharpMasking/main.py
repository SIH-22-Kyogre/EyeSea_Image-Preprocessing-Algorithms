import os
import numpy as np
import natsort
import xlwt
from skimage import filters, io
import cv2

from config import config

def run(base_path=None, input_dirname=None, output_dirname=None):

	if base_path is None:
		base_path = config.get('BASE_PATH')
	if input_dirname is None:
		input_dirname = config.get('INPUT_DIRNAME')
	if output_dirname is None:
		output_dirname = config.get('OUTPUT_DIRNAME')

	in_path = os.path.join(base_path, input_dirname)
	out_path = os.path.join(base_path, output_dirname)
	files = os.listdir(in_path)
	files =  natsort.natsorted(files)
	before_paths = []
	after_paths = []

	for i in range(len(files)):
		file = files[i]
		if file in config.get('IGNORE_FILES'):
			continue
			
		filepath = os.path.join(in_path, file)
		prefix = file.split('.')[0]
		format_ = file.split('.')[1]
		if os.path.isfile(filepath):
			print('Working on', file)
			before_paths.append(os.path.join(in_path, file))
			img = io.imread(before_paths[-1])

			sceneRadiance = filters.unsharp_mask(img, multichannel=True, radius=4, amount=2)

			after_paths.append(os.path.join(out_path, prefix + '_UMASK.' + format_))
			io.imsave(after_paths[-1], sceneRadiance)
	
	return (before_paths, after_paths)
