import os
import numpy as np
import cv2
import natsort


from .DetermineDepth import determineDepth
from .getAtomsphericLight import getAtomsphericLight
from .getRefinedTramsmission import Refinedtransmission
from .getScatteringRate import ScatteringRateMap
from .getSceneRadiance import SceneRadiance
from .getTransmissionGB import TransmissionGB
from .getTransmissionR import TransmissionR
    
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
	files = natsort.natsorted(files)
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

			blockSize = 9
			largestDiff = determineDepth(img, blockSize)
			AtomsphericLight = getAtomsphericLight(largestDiff, img)
			print('AtomsphericLight',AtomsphericLight)
			sactterRate = ScatteringRateMap(img, AtomsphericLight, blockSize)
			transmissionGB = TransmissionGB(sactterRate)
			transmissionR = TransmissionR(transmissionGB, img, blockSize)
			transmissionGB, transmissionR = Refinedtransmission(transmissionGB, transmissionR, img)
			sceneRadiance = SceneRadiance(img, transmissionGB, transmissionR, sactterRate, AtomsphericLight)

			after_paths.append(os.path.join(out_path, prefix + '_NOM.' + format_))
			cv2.imwrite(after_paths[-1], sceneRadiance)
	
	return (before_paths, after_paths)