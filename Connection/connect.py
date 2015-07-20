# -*- coding:utf-8 -*-
# Script to be run on Client AWS to connect the APK Server with NFS.
# corresponding script is disconnect.py .
__author__ = 'Marchon'
__createTime__ = '20150720'

# ------------------------- Config -------------------------

# Number of Directories storing apk
# apk0, apk1, apk2, ..., apk[NUM_APK_DIR - 1]
NUM_APK_DIR = 8

# Base path for directories storing apk on the host
# A number will be appended to the end of this path to complete the path
BASE_APK_DIR = "/home/lsuper/apk_data/apk"

# NFS port
NFS_PORT = 2049

# where EBS volume is mounted, now is pdev instance
# Do not commit plaintext server ip to Github
HOST = "XXX.XXX.XXX.XXX"

# ------------------------- Configuration -------------------------

import subprocess


def mountAPKDir(num):
    cmd = ("sudo mount -t nfs -o addr=%s,proto=tcp,port=%d %s:%s%d/ "
           "/home/ubuntu/apk%d") % (HOST, NFS_PORT, HOST, BASE_APK_DIR, num, num)
    subprocess.check_output(cmd, shell=True)

if __name__ == "__main__":
    # Mount all APK directories on the remote
    print "Mounting apk directories..."
    for i in xrange(0, NUM_APK_DIR):
        subprocess.call(["mkdir", "/home/ubuntu/apk" + str(i)])
        mountAPKDir(i)