"""
The module provide a quick way to run the provinance filtering test.

Usage: batch_process.py dataset [option]

dataset: datasets to index.
   Supported: NC2017_Dev1_Beta4, NC2017_Dev2_Beta1, ...

General options:
    
    -gt_name           name of dataset use to evaluate, effective when set use_gt (for test only!!)
    
    -run_dir           directory where the training code is (default ../Model_Training/src/)
    
    -mediscore_dir     directory of Mediscore (default /home/xuzhang/project/Medifor/code/MediScore/)

Output:
    
    output and json file in output directory
    
    score and log files in score and log derectory

Examples:
    
    Train the index and do the search    

    >>> python batch_process.py NC2017_Dev1_Beta4
    
    >>> python batch_process.py NC2017_Dev2_Beta1 
"""

#! /usr/bin/env python2

import numpy as np
import scipy.io as sio
import time
import os
import sys
import pandas as pd
import subprocess
import argparse
import time

####################################################################
# Parse command line
####################################################################


def usage():
    print >>sys.stderr, \
    """
    The module provide a quick way to run the provinance filtering test.
    
    Usage: batch_process.py dataset [option]
    
    dataset: datasets to index.
       Supported: NC2017_Dev1_Beta4, NC2017_Dev2_Beta1, ...
    
    General options:
        -gt_name           name of dataset use to evaluate, effective when set use_gt (for test only!!)
        
        -run_dir           directory where the training code is (default ../Model_Training/src/)
        
        -mediscore_dir     directory of Mediscore (default /home/xuzhang/project/Medifor/code/MediScore/)
    
    Output:
        output and json file in output directory
        score and log files in score and log derectory
    
    Examples:
        
        Train the index and do the search    
    
        >>> python batch_process.py NC2017_Dev1_Beta4
        
        >>> python batch_process.py NC2017_Dev2_Beta1 
    """
    sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--dbname", nargs='?', type=str, default = 'MFC18_Dev1_Ver2',
                        help="Database dataset name")

    parser.add_argument("--root_dir", nargs='?', type=str, default = '/home/xuzhang/project/Medifor/data/',
                        help="Directory where dataset stores")

    parser.add_argument("--output_dir", nargs='?', type=str,\
            default = '/home/xuzhang/project/Medifor/code/Genealogy_Graph_Building/',
            help="Directory where index file stores")

    parser.add_argument("--setting", nargs='?', type=str, default = '',
                        help="Directory where index file stores")

    args = parser.parse_args()
    
    if 'MFC18' in args.dbname or 'NC2017' in args.dbname:
        ndataset_list = args.dbname.split('_')
        index_name = ndataset_list[0]+'_'+ndataset_list[1]
    else:
        index_name = args.dbname

    root_dir = args.root_dir + args.dbname + '/'
    system_output_dir = args.output_dir + 'output/' + args.dbname + '/'

    output_directory = args.output_dir + 'score/{}/'.format(args.dbname)
    index_file = root_dir + 'indexes/' + index_name + '-provenance-index.csv'
    reference_file = root_dir + 'reference/provenance/' + index_name + '-provenance-ref.csv'
    reference_node_file = root_dir + 'reference/provenance/' + index_name + '-provenance-ref-node.csv'
    world_file = root_dir + 'indexes/' + index_name + '-provenance-world.csv'
    reference_dir = root_dir 
    system_output_file = system_output_dir + 'output.csv'

    extract_command = "python ./ProvenanceGraphBuildingScorer.py "\
                   + " -o {}".format(output_directory) \
    		   + " -x {}".format(index_file) \
    		   + " -r {}".format(reference_file) \
    		   + " -n {}".format(reference_node_file) \
    		   + " -w {}".format(world_file) \
    		   + " -R {}".format(reference_dir) \
    		   + " -s {}".format(system_output_file) \
    		   + " -S {}".format(system_output_dir)

    subprocess.call(extract_command,shell=True)
