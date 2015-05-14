#!/usr/bin/env python3
"""
This is not necessarily an efficient way of doing things by downloading ASCII per Madrigal remote filter
and then converting to hdf5 locally, rather we want to download just HDF5, but it's a OK way to start.

Tests loading of globalisprint ascii file, resaving as HDF5 for fast data processing
first I clunkily used
globalIsprint.py --verbose --url=http://isr.sri.com/madrigal --parms=DNE,AZM,ELM,NE,UT1 --output=example.txt --startDate="01/01/1950" --endDate="10/31/2007" --inst=61 --kindat=0 --filter azm,90,270
then I ran the code below.
It took many minutes to filter the data remotely (would have taken ~ minute using pandas/hdf5 I believe),
"""
from numpy import loadtxt #should consider perhaps genfromtxt to handle "missing" values
import h5py
from os.path import splitext,expanduser

def txt2h5(fn):
    h5fn = splitext(expanduser(fn))[0] + '.h5'

    gc=(1,2,4) # a priori based on the specific globalisprint command, and that numpy.loadtxt can't handle non-numeric values


    # get column names
    with open(fn,'r') as f:
        head = f.readline().split()

    # load data, here I lazily used from my globalisprint command that columns 1,2,5 were good data
    arr = loadtxt(fn,skiprows=1,usecols=gc)
    with h5py.File(h5fn,'w',libver='latest') as f:
        for i,c in enumerate(gc): #because we only read "good" columns
            f[head[c]] = arr[:,i]

if __name__ == '__main__':
    from sys import argv
    txt2h5(argv[1])
