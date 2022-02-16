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

def get_logger1(logger_level):
               
    # Create a custom logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    print('HEYHEY')

    # Streaming Handler
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    logger.addHandler(c_handler)

    # File Handler
    #f_handler = logging.FileHandler('file.log')
    #f_handler.setLevel(logging.DEBUG)
    #f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #f_handler.setFormatter(f_format)
    #logger.addHandler(f_handler)
    
    return logger


def get_logger2(logger_level, create_file=False):

    # create logger for prd_ci
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    print('HEY')

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if create_file:
        # create file handler for logger.
        fh = logging.FileHandler('SPOT.log')
        fh.setLevel(level=logging.DEBUG)
        fh.setFormatter(formatter)
    # reate console handler for logger.
    ch = logging.StreamHandler()
    ch.setLevel(level=logging.DEBUG)
    ch.setFormatter(formatter)

    # add handlers to logger.
    if create_file:
        log.addHandler(fh)

    log.addHandler(ch)
    return log 

# -----------------------------------------------------------------------------

# Debug levels:
# CRITICAL  50
# ERROR 	40
# WARNING 	30
# INFO      20
# DEBUG 	10
# NOTSET 	0

def get_logger(log_level):
    #print('--> Log_level', log_level)
    logger = logging.getLogger()
    
    logger.handlers = []
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    logger.setLevel(log_level)
    
    logging.info('Logger initialized with level {}'.format(log_level))
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