import math
import os
import natsort
import numpy as np
import datetime
import cv2
from skimage.color import rgb2hsv

from .color_equalisation import RGB_equalisation
from .global_stretching_RGB import stretching
from .hsvStretching import HSVStretching

from .histogramDistributionLower import histogramStretching_Lower
from .histogramDistributionUpper import histogramStretching_Upper
from .rayleighDistribution import rayleighStretching
from .rayleighDistributionLower import rayleighStretching_Lower
from .rayleighDistributionUpper import rayleighStretching_Upper
from .sceneRadiance import sceneRadianceRGB

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
			img = cv2.imread(before_paths[-1])

			height = img.shape[0]
			width = img.shape[1]
			sceneRadiance = RGB_equalisation(img, height, width)
			sceneRadiance = stretching(sceneRadiance)
			sceneRadiance_Lower, sceneRadiance_Upper = rayleighStretching(sceneRadiance, height, width)
			sceneRadiance = (np.float64(sceneRadiance_Lower) + np.float64(sceneRadiance_Upper)) / 2
			sceneRadiance = HSVStretching(sceneRadiance)
			sceneRadiance = sceneRadianceRGB(sceneRadiance)
			
			after_paths.append(os.path.join(out_path, prefix + '_RDist.' + format_))
			cv2.imwrite(after_paths[-1], sceneRadiance)
	
	return (before_paths, after_paths)
