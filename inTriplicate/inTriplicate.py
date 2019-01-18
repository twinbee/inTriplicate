#!/usr/bin/python
import argparse
import glob; 
import os
import fnmatch
import subprocess

__author__ = 'twinbee'

 
parser = argparse.ArgumentParser(description='InTriplicate')
parser.add_argument('-s','--source', help='SD/Flash drive location',required=True)
parser.add_argument('-d','--destination',help='Copy to file location', required=False, default=None)
parser.add_argument('-b','--burn',help='Burn a disc (Not Yet Implemented)', required=False, default=False)
parser.add_argument('-r','--refresh',help='Refresh flash (Not Yet Implemented)', required=False, default=True)
parser.add_argument('-g','--gallery',help='Generate web galleries (Not Yet Implemented)', required=False, default=False)
parser.add_argument('-p','--parity',help='Generate parity files using am installed par2', required=False, default=False)

args = parser.parse_args()
 
## show values ##
print ("Input file: %s" % args.source )
print ("destination: %s" % args.destination )
print ("Burn: %s" % args.burn )
print ("Refresh: %s" % args.refresh )
print ("Parity: %s" % args.parity )
print ("Gallery: %s" % args.gallery )

def recursive_walk(folder):
    par2Path = "bin/par2.exe" 

    for folderName, subfolders, filenames in os.walk(folder):
        if subfolders:
            for subfolder in subfolders:
                recursive_walk(subfolder)
        print('\nFolder: ' + folderName + '\n')
        for filename in filenames:
            print(filename + '\n')
            if (args.parity):
            	subprocess.run([par2Path, "c", "-r5", folderName + "/" +filename])

recursive_walk(args.source)