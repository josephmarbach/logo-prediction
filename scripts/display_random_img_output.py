r"""Script for generating and displaying random subsample of df_img_predict

Run as: ipython --pdb -- ./scripts/display_random_img_output.py \
    --func get_specified_data_paths --func_args 1355 1420
"""

import argparse
import numpy as np
import os
import pandas as pd
import random

import matplotlib

import autil
from autil import get_new_images, get_specified_data_paths, ipynb_kernel_used
from database import db_img_predict, get_rand_samp_df
from putil import display_results

# if python kernel, is used set this to the keyval of the file to read
#  if None no file will be loaded
KEYVAL = None
# number of random images to display:
SAMPLE_NUMBER = 10

def parse_args():
    r"""Parse CLI arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dpi', help='Plotting dots per inch for images'
    )
    parser.add_argument(
        '--func', help='Function used to get list of images to plot'
    )
    parser.add_argument(
        '--func_args', nargs='+', action='append',
        help='Arguments used for plotting function'
    )
    parser.add_argument(
        '--keyval', help='DataFrame read keyvalue'
    )
    parser.add_argument(
        '--margin', help='Plotting margin for images'
    )
    parser.add_argument(
        '--sample_number', type=int, help='Number of random images to display'
    )
    args = parser.parse_args()
    return args


def main():
    r"""Main"""
    sample_number = SAMPLE_NUMBER
    if ipynb_kernel_used():
        keyval = main_keyval
        if KEYVAL is None:
            # manual value setting for running a kernel within this script:
            # keyval = '46304102553087547621'
            None  # None here to avoid error if keyval above is commented out
    else:
        args = parse_args()
        keyval = args.keyval
        if args.sample_number:
            sample_number = args.sample_number
    if keyval is None:
        if args.func is None:
            db_rand, tup_results = get_rand_samp_df(samp_num=sample_number)
        else:
            func_a=autil.FUNCTION_MAP[args.func]
            db_rand, tup_results = get_rand_samp_df(samp_num=sample_number,
                                                    args=args.func_args,
                                                    func=func_a)
        lst_url_data = tup_results[0]
        keyval = tup_results[1]
        get_new_images(lst_url_data)
    else:
        db_rand = db_img_predict()
        db_rand.df_read_w_key(read_key=keyval)
    display_results(df=db_rand.df)


if __name__ == '__main__':
    main()
