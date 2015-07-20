__author__ = 'Marchon'

from connect import *

import subprocess

def umountAPKDir(num):
  cmd = ("sudo umount -f -l /home/ubuntu/apk%d") % (HOST, NFS_PORT, HOST, BASE_APK_DIR, num, num)
  subprocess.check_output(cmd, shell=True)

if __name__ == "__main__":
  # Mount all APK directories on the remote
  print "Mounting apk directories..."
  for i in xrange(0, NUM_APK_DIR):
    umountAPKDir(i)

