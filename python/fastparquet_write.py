from concurrent.futures import ProcessPoolExecutor, wait
from multiprocessing import Manager
from argparse import ArgumentParser
from concurrent.futures import Future
from typing import List, Dict

import fastparquet
import os
import pandas as pd
import numpy as np

def worker(fname, write_lock, page_num):
    n_cols = 10
    n_rows = int(1e5)
    df = pd.DataFrame(
        np.ones(shape=(n_rows, n_cols), dtype=np.float32),
        columns=[f"col_{i}" for i in range(n_cols)]
    )

    with write_lock:
        fastparquet.write(
            filename=fname, 
            data=df, 
            file_scheme='simple',
            append=(os.path.exists(fname))
        )

        size = os.path.getsize(fname)

        print(f"Wrote page {page_num} - {size} bytes...")

def on_complete(f: Future):
    e = f.exception()
    if(e is not None):
        raise e
    
def main(n_procs=8, n_data_chunks=128, fname=None):
    if(fname is None):
        raise "fname argument cannot be None"

    mgr = Manager()
    
    write_lock = mgr.Lock()
    futures: List[Future] = []

    with ProcessPoolExecutor(max_workers=n_procs) as pool:
        for i in range(n_data_chunks):
            f = pool.submit(worker, fname, write_lock, i)
            futures.append(f)
            f.add_done_callback(on_complete)

        wait(futures)

    print(f"Wrote {fname}.")    
    mgr.shutdown()
        

if(__name__ == "__main__"):
    parser = ArgumentParser()
    parser.add_argument("--n_procs", default=8)
    parser.add_argument("--n_data_chunks", default=30)
    parser.add_argument("--fname", default="/var/tmp/test.parquet")
    args = parser.parse_args()

    if(os.path.exists(args.fname)):
        os.remove(args.fname)
    
    print(f"Writing to {args.fname}...")

    kwargs = vars(args)
    main(**kwargs)