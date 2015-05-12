#!/usr/bin/env python2
"""
basic example of using Madrigal to query data
Michael Hirsch
https://scivision.co/madrigal-api-install-and-basic-example-for-geospace-remote-sensing-query/

This should download a bunch
"""
from __future__ import print_function,division
from six import PY3
if PY3:
    exit('currently Madrigal is for Python<=2.7 (sigh)')
#
try:
    from madrigalWeb import madrigalWeb as MW
except ImportError as e:
    exit('you must install madrigal first. https://scivision.co/madrigal-api-install-and-basic-example-for-geospace-remote-sensing-query/   {}'.format(e))
#
from pandas import Series,DataFrame
from datetime import datetime
from os.path import join


def madname2code(madobj,instreq):
    """
    instreq: string or list of strings of instrument names you want madrigal integer code(s) for
    """
    print('downloading instrument codes')
    instobj = madobj.getAllInstruments() # list() of instrument objects

    #put the names and codes in a nicely indexable Pandas Series
    instcodes= Series(index=[i.name.decode('utf8') for i in instobj],
                      data= [i.code for i in instobj])

    return instcodes[instreq] #get the instrument codes requested


def getexpdata(madobj,code,odir):
    """
    gets all experiments for all available times (between years 1900 and 2100)
    note month and day canNOT be 0 or you'll get an empty list in return
    code: instrument code from Pandas Series
    """
    # this is list of all experiments for this instrument for all time
    # iterate over this to get data files for each experiment
    print('downloading experiment codes')
    exps = madobj.getExperiments(code,1900,1,1,0,0,0,2100,1,1,0,0,0,local=1)
    # let's put this experiment list in a user-friendly format
    # there might be a better way to do this to allow better querying vs. time
    experiments = DataFrame(index=[e.id for e in exps],columns=['start','end','fn'])
    for e in exps:
        experiments.at[e.id,'start'] = datetime(year=e.startyear, month=e.startmonth,
                                    day=e.startday,hour=e.starthour,minute=e.startmin,
                                    second=e.startsec)
        experiments.at[e.id,'end']   = datetime(year=e.endyear, month=e.endmonth,
                                    day=e.endday,hour=e.endhour,minute=e.endmin,
                                    second=e.endsec)
#%%
    exparams=[]
    for i in experiments.index:
        print('downloading experiment id {} '.format(i))
        expfile = madobj.getExperimentFiles(i)
        experiments.at[i,'fn'] = expfile.name

        exparams.append(madobj.getExperimentFileParameters(expfile))

       #not yet
        #ofn = join(odir,expfile.name)
       #print('saving {}'.format(ofn))
        #madobj.downloadFile(expfile, ofn,"hdf5")

    return experiments,exparams

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description="basic example of using Madrigal")
    p.add_argument('--madurl',help='url of madridgal database',type=str,default='http://isr.sri.com/madrigal/')
    p.add_argument('--odir',help='output directory to cache madridgal data in',type=str,default='maddata')
    p.add_argument('-i','--inst',help='instrument to access',type=str,default='Poker Flat IS Radar')
    p = p.parse_args()
#%%
    print('downloading madrigal site object')
    madobj = MW.MadrigalData(p.madurl) #this has several methods

    pfisr={'code':madname2code(madobj,p.inst)} #get the PFISR code

    experiments,exparams = getexpdata(madobj,pfisr['code'],p.odir)
