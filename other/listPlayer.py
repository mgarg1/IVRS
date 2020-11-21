#!/usr/bin/python

import os,sys

# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)


def playWord(filename):
    cmdToRun = 'cvlc  %s  --play-and-exit --no-osd > /dev/null 2>&1' % (filename)
    if os.path.isfile(filename):
        #print ("File exist")
        os.system(cmdToRun)
    else:
        print('FILE NOT FOUND %s' % (filename))

for i in sys.argv:
    playWord(i)
