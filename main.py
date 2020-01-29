import uCAMIII
import time
import sys
import os

cam = uCAMIII.UCam()
synced = cam.sync()
print("synced is ready? {}".format(synced))

if synced:
    cam.take_picture('test.png')

cam.ser.close()