from argparse import ArgumentParser
import pyarrow.parquet as pq

def main(fname=None):
    print(f"Reading {fname}...")

    pf = pq.ParquetFile(fname)
    print(f"Total rows in file: {pf.metadata.num_rows}")

if(__name__ == "__main__"):
    parser = ArgumentParser()
    parser.add_argument("--fname", default="/var/tmp/test.parquet")
    args = parser.parse_args()
    
    kwargs = vars(args)
    main(**kwargs)