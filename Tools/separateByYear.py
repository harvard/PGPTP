#!/usr/bin/env python
'''
Created on Oct 13, 2014

@author: waldo
'''

import sys
import os
import csv

def makeOutFile(outdict, term, fname, header):
    outfile = csv.writer(open(term + '/' + fname, 'w'))
    outdict[term] = outfile
    outfile.writerow(header)

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print 'Usage: separateByYear csvFile'
        sys.exit(1)
        
    fname = sys.argv[1]
    
    fin = csv.reader(open(fname, 'rU'))
    header = fin.next()
    outdict = {}
    for l in fin:
        term = l[1]
        if term not in outdict:
            makeOutFile(outdict, term, fname, header)
        outdict[term].writerow(l)