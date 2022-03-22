import matplotlib.pyplot as plot
import sys
import cv2

import DCP as dcp 
import LowComplexityDCP as lc_dcp
import GBdehazingRCorrection as gbrc
import IBLA as ibla
import MIP as mip
import NewOpticalModel as nom
import RoWS as rows
import UDCP as udcp
import ULAP as ulap
import UnsharpMasking as umask

import sys

if __name__ == '__main__':
    # before_paths, after_paths = dcp.run()
    # before_paths, after_paths = lc_dcp.run()
    # before_paths, after_paths = gbrc.run()
    # before_paths, after_paths = ibla.run()
    # before_paths, after_paths = mip.run()
    # before_paths, after_paths = nom.run() 
    # before_paths, after_paths = rows.run()
    # before_paths, after_paths = udcp.run()
    # before_paths, after_paths = ulap.run()
    

    if len(sys.argv)>1 and '--visualize' in sys.argv:
        for before, after in zip(before_paths, after_paths):
            before_img = cv2.imread(before)
            after_img = cv2.imread(after)
            fig, (ax1, ax2) = plot.subplots(1, 2)
            ax1.imshow(before_img)
            ax2.imshow(after_img)
            plot.show()

