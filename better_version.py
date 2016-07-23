#!/usr/bin/env python

from __future__ import with_statement
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
from functools import partial
import struct
import glob
import math
import os
from os.path import basename
import shutil
import fnmatch
import re
REGEX = re.compile(r'\d+')


def coordinates_filename(where):                    #given file returns coordinates
    return REGEX.findall(basename(where))



def get_sample(where):
    longtitude_diff = 0.0174533  # pi/180 radians
    area_factor = 6371 * 6371 * 1000000
    paths = []
    
    ar_vol = [0]*100
    ar_vol_tmp = [0]*100
    for root, dirnames, filenames in os.walk(where):        #walks subdirs of where
        for filename in fnmatch.filter(filenames, '*.hgt'):
            paths.append(os.path.join(root, filename))
    for path in paths:
        print path
        coords = coordinates_filename(path)
        m = float(coords[0])
        coords[0] = math.radians(m)
        coords[1] = math.radians(m + 1)
        area = int(area_factor * abs(longtitude_diff * (math.sin(coords[1]) - math.sin(coords[0]))))    #area of grid cell
        with open(path, "rb") as height_f:
            for buf in iter(partial(height_f.read, 2), ''):  # Read two bytes at a time until read returns nothing.
                val = struct.unpack('>h', buf)[0]  # ">h" is a signed two byte
                if val == -32768 or val >= 100:
                    continue
		if val < 0:
		    ar_vol[0] += abs(val)*1442401 / area		#for depressions
		else:
		    ar_vol_tmp[val]+=1					#adds value to correct place
        for i in range(0,100):
	    if ar_vol_tmp[i]!=0:       
        	ar_vol[i] += ar_vol_tmp[i]*1442401 / area

    return ar_vol


def unzipmon(path):
    zipnam1e = path.split('.', 1)[0]
    os.makedirs(zipnam1e)                        #makes directory for files(makes them reusable for unlimitez zip/unzip)
    with closing(ZipFile(path, "r")) as z:
        z.extractall(zipnam1e)                    #unzips


def zipdir(basedir, archivename):
    assert os.path.isdir(basedir)
    os.remove(archivename)                        #deletes oldzip
    with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as zip_f:
        for root, dirs, files in os.walk(basedir):
                                    #NOTE: ignore empty directories
            for fn in files:
                absfn = os.path.join(root, fn)
                zfn = absfn[len(basedir)+len(os.sep):]     #XXX: relative path
                zip_f.write(absfn, zfn)
    shutil.rmtree(basedir)                        #deletes old folder


def main():
    paths = glob.glob(os.path.expanduser("~/project/*.zip"))
                    #should be cwd, contain all zips
    water_volume_tmp=[0]*100				#list contains area of land at 0m, 1m .. to 99m.
    water_volume=[0]*100

    #while e > 0 and n != 100:                        #repeats everything until volume is expended or sea level of 100 is reached
    for path in paths:                #cycles all zipfiles
         dispath = os.path.realpath(path)        #path to zipfile
         unzipmon(path)               #file needs to be zipped back in same step!!
         zipname = dispath.split('.', 1)[0]        #path to unzipped folder(by removing extension)
         print dispath, zipname
                                #actions to unzipped files
	 water_volume_tmp = get_sample(zipname)
	 for i in range(0,100):
	       water_volume[i] += water_volume_tmp[i]
	 shutil.rmtree(zipname)			#removes folder, as zip isn't deleted no need to zip it
         #zipdir(zipname, path)            #zips
	 print water_volume
	 with open("results.txt", "a") as results_f:
             print >>results_f, " %s " % (water_volume),


if __name__ == '__main__':
    main()
