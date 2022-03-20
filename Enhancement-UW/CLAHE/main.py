import os
import numpy as np
import cv2
import natsort
import xlwt
from skimage import exposure

from .sceneRadianceCLAHE import RecoverCLAHE
from .sceneRadianceHE import RecoverHE

from config import config

def run(base_path=None, input_dirname=None):

	if base_path is None:
		base_path = config.get('BASE_PATH')
	if input_dirname is None:
		input_dirname = config.get('INPUT_DIRNAME')

	path = os.path.join(base_path, input_dirname)
	files = os.listdir(path)
	files =  natsort.natsorted(files)
	for i in range(len(files)):
		file = files[i]
		filepath = path + "/" + file
		prefix = file.split('.')[0]
		if os.path.isfile(filepath):
			print('********    file   ********',file)
			# img = cv2.imread('InputImages/' + file)
			img = cv2.imread(folder + '/InputImages/' + file)
			sceneRadiance = RecoverCLAHE(img)
			# cv2.imwrite('OutputImages/' + prefix + '_CLAHE.jpg', sceneRadiance)
			cv2.imwrite('Temps/' + prefix + '_CLAHE.jpg', sceneRadiance)
