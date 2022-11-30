import os
from argparse import ArgumentParser
import fastparquet

def main(fname=None):
    print(f"Reading {fname}...")

    pf = fastparquet.ParquetFile(fname)
    print(f"Total rows in file: {pf.count()}")

if(__name__ == "__main__"):
    parser = ArgumentParser()
    parser.add_argument("--fname", default="/var/tmp/test.parquet")
    args = parser.parse_args()
    
    kwargs = vars(args)
    main(**kwargs)