import os
import datetime
import numpy as np
import cv2
import natsort

from .CloseDepth import closePoint
from .F_stretching import StretchingFusion
from .MapFusion import Scene_depth
from .MapOne import max_R
from .MapTwo import R_minus_GB
from .blurrinessMap import blurrnessMap
from .getAtomsphericLightFusion import ThreeAtomsphericLightFusion
from .getAtomsphericLightOne import getAtomsphericLightDCP_Bright
from .getAtomsphericLightThree import getAtomsphericLightLb
from .getAtomsphericLightTwo import getAtomsphericLightLv
from .getRGbDarkChannel import getRGB_Darkchannel
from .getRefinedTransmission import Refinedtransmission
from .getTransmissionGB import getGBTransmissionESt
from .getTransmissionR import getTransmission
from .global_Stretching import global_stretching
from .sceneRadiance import sceneRadianceRGB
from .sceneRadianceHE import RecoverHE

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
			n = 5
			RGB_Darkchannel = getRGB_Darkchannel(img, blockSize)
			BlurrnessMap = blurrnessMap(img, blockSize, n)
			AtomsphericLightOne = getAtomsphericLightDCP_Bright(RGB_Darkchannel, img, percent=0.001)
			AtomsphericLightTwo = getAtomsphericLightLv(img)
			AtomsphericLightThree = getAtomsphericLightLb(img, blockSize, n)
			AtomsphericLight = ThreeAtomsphericLightFusion(AtomsphericLightOne, AtomsphericLightTwo, AtomsphericLightThree, img)

			R_map = max_R(img, blockSize)
			mip_map = R_minus_GB(img, blockSize, R_map)
			bluriness_map = BlurrnessMap

			d_R = 1 - StretchingFusion(R_map)
			d_D = 1 - StretchingFusion(mip_map)
			d_B = 1 - StretchingFusion(bluriness_map)

			d_n = Scene_depth(d_R, d_D, d_B, img, AtomsphericLight)
			d_n_stretching = global_stretching(d_n)
			d_0 = closePoint(img, AtomsphericLight)
			d_f = 8  * (d_n +  d_0)

			transmissionR = getTransmission(d_f)
			transmissionB, transmissionG = getGBTransmissionESt(transmissionR, AtomsphericLight)
			transmissionB, transmissionG, transmissionR = Refinedtransmission(transmissionB, transmissionG, transmissionR, img)
			sceneRadiance = sceneRadianceRGB(img, transmissionB, transmissionG, transmissionR, AtomsphericLight)
			
			after_paths.append(os.path.join(out_path, prefix + '_IBLA.' + format_))
			cv2.imwrite(after_paths[-1], sceneRadiance)
	
	return (before_paths, after_paths)

