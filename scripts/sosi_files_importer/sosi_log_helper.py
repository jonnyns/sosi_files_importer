# -*- coding: utf-8 -*-
"""
Copyright © 2022 Jonny Normann Skålvik

Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the “Software”), to deal 
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in 
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.

This file is part of SosiImporter, an addon to import SOSI files containing
3D model data into Blender.
"""

import numpy as np
import logging

# -----------------------------------------------------------------------------

# Debug levels:
# CRITICAL  50
# ERROR 	40
# WARNING 	30
# INFO      20
# DEBUG 	10
# NOTSET 	0

def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.info('Logger initialized')
    return logger

# -----------------------------------------------------------------------------

def printArray(ary):
    for row in range(len(ary)):
        for col in range (len(ary[row])):
            print("{:8.3f}".format(ary[row][col]), end = " ")
        print()
        
# -----------------------------------------------------------------------------
        
def formatArray(ary, leadtxt=None):
    #print(type(ary))
    if type(ary) is tuple or type(ary) is list:
        ary = np.asarray(ary)
    elif not isinstance(ary, np.ndarray):
        return ''
    s = np.array2string(ary, precision=3, separator=' ')
    if (leadtxt != None):   
        s = leadtxt + '\n' + s
    return s