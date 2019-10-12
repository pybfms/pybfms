'''
Created on Oct 11, 2019

@author: ballance
'''
import os


def hdl_path(file, *args):
    '''
    Returns the path to a file with the 'hdl' subdirectory 
    of the package in which 'file' is located
    '''
    return os.path.join(
        os.path.dirname(os.path.abspath(file)),
        "hdl", *args)
    