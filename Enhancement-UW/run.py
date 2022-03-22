import matplotlib.pyplot as plot
import sys
import cv2

import CLAHE as clahe
import GC as gc
import ICM as icm
import HE as he
import RayleighDistribution as r_dist
import RGHS as rghs
import UCM as ucm
import UnsharpMasking as umask
import BilateralFilter as bf

if __name__ == '__main__':
    # before_paths, after_paths = clahe.run()
    # before_paths, after_paths = gc.run()
    # before_paths, after_paths = icm.run()
    # before_paths, after_paths = he.run()
    # before_paths, after_paths = r_dist.run()
    # before_paths, after_paths = rghs.run()
    # before_paths, after_paths = ucm.run()
    before_paths, after_paths = umask.run()
    # before_paths, after_paths = bf.run()

    if len(sys.argv)>1 and '--visualize' in sys.argv:
        for before, after in zip(before_paths, after_paths):
            before_img = cv2.imread(before)
            after_img = cv2.imread(after)
            fig, (ax1, ax2) = plot.subplots(1, 2)
            ax1.imshow(before_img)
            ax2.imshow(after_img)
            plot.show()