#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Tomoki Hayashi
#  MIT License (https://opensource.org/licenses/MIT)

"""Calculate statistics of feature files."""

import argparse
import logging
import os

import numpy as np
import yaml

from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

from parallel_wavegan.datasets import MelDataset
from parallel_wavegan.utils import read_hdf5
from parallel_wavegan.utils import write_hdf5


def main():
    """Run preprocessing process."""
    parser = argparse.ArgumentParser(
        description="Compute mean and variance of dumped raw features "
                    "(See detail in parallel_wavegan/bin/compute_statistics.py).")
    parser.add_argument("--rootdir", type=str, required=True,
                        help="directory including feature files.")
    parser.add_argument("--config", type=str, required=True,
                        help="yaml format configuration file.")
    parser.add_argument("--dumpdir", default=None, type=str,
                        help="directory to save statistics. if not provided, "
                             "stats will be saved in the above root directory. (default=None)")
    parser.add_argument("--verbose", type=int, default=1,
                        help="logging level. higher is more logging. (default=1)")
    args = parser.parse_args()

    # set logger
    if args.verbose > 1:
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s")
    elif args.verbose > 0:
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s")
    else:
        logging.basicConfig(
            level=logging.WARN, format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s")
        logging.warning('Skip DEBUG/INFO messages')

    # load config
    with open(args.config) as f:
        config = yaml.load(f, Loader=yaml.Loader)
    config.update(vars(args))

    # check directory existence
    if args.dumpdir is None:
        args.dumpdir = os.path.dirname(args.rootdir)
    if not os.path.exists(args.dumpdir):
        os.makedirs(args.dumpdir)

    # get dataset
    mel_query = "*.npy"
    mel_load_fn = np.load
    dataset = MelDataset(
        args.rootdir,
        mel_query=mel_query,
        mel_load_fn=mel_load_fn)
    logging.info(f"The number of files = {len(dataset)}.")

    # calculate statistics
    scaler = StandardScaler()
    for mel in tqdm(dataset):
        scaler.partial_fit(mel)

    stats = np.stack([scaler.mean_, scaler.scale_], axis=0)
    np.save(os.path.join(args.dumpdir, "stats.npy"), stats.astype(np.float32), allow_pickle=False)


if __name__ == "__main__":
    main()
