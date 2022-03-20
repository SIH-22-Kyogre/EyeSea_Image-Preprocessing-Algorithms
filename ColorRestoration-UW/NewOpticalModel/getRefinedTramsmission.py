import numpy as np
from .GuidedFilter import GuidedFilter

def Refinedtransmission(transmissionGB, transmissionR, img):

    gimfiltR = 50  
    eps = 10 ** -3  

    guided_filter = GuidedFilter(img, gimfiltR, eps)
    transmissionGB = guided_filter.filter(transmissionGB)
    transmissionR = guided_filter.filter(transmissionR)

    transmissionGB = np.clip(transmissionGB,0.1, 0.9)
    transmissionR = np.clip(transmissionR,0.1, 0.9)

    return transmissionGB,transmissionR
