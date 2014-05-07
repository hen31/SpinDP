from SpinOS import SpinOS
import atexit
__author__ = 'Hendrik'

SpinOs = SpinOS()

@atexit.register
def goodbye():
    SpinOs.shutdown()
    print("SPIN OS is DEAD")