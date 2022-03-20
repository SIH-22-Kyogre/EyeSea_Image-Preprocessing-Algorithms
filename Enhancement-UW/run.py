import CLAHE as clahe
import GC as gc
import ICM as icm
import HE as he
import RayleighDistribution as r_dist
import RGHS as rghs
import UCM as ucm

if __name__ == '__main__':
    # before_after_paths = clahe.run()
    # before_paths, after_paths = gc.run()
    # before_paths, after_paths = icm.run()
    # before_paths, after_paths = he.run()
    # before_paths, after_paths = r_dist.run()
    # before_paths, after_paths = rghs.run()
    before_paths, after_paths = ucm.run()