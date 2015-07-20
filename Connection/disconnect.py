__author__ = 'Marchon'

from connect import *

import subprocess


def umount_apk_dir(num):
    cmd = "sudo umount /home/ubuntu/apk%d" % num
    subprocess.check_output(cmd, shell=True)

if __name__ == "__main__":
    # Mount all APK directories on the remote
    print "Mounting apk directories..."
    for i in xrange(0, NUM_APK_DIR):
        umount_apk_dir(i)

