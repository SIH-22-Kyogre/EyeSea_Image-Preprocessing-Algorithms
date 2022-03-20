import DCP as dcp 
import LowComplexityDCP as lc_dcp
import GBdehazingRCorrection as gbrc
import IBLA as ibla
import MIP as mip

if __name__ == '__main__':
    # before_paths, after_paths = dcp.run()
    # before_paths, after_paths = lc_dcp.run()
    # before_paths, after_paths = gbrc.run() !!!
    # before_paths, after_paths = ibla.run()
    before_paths, after_paths = mip.run()
