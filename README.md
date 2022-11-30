# Fastparquet file-append issue...

This repository contains code so as to demonstrate something pretty simple. 

If I use the `fastparquet` library to write a parquet file such that I repeatedly append to the file as follows:

```
fastparquet.write(
    filename=fname, 
    data=df, 
    file_scheme='simple',
    append=True
)
```

I find that if I then read that file back into `fastparquet` and query the total row count, it returns the correct aggregate row count from all the writes. 

However, if I take that same fastparquet file and again read it with `pyarrow`, this time if I query the number of rows in the file I will instead get the number of rows _in a single write_. I should get the aggregate total...

The code contained in this repository is broken un between languages and parquet frameworks. There is only one script to write the parquet dataset, in `python/fastparquet_write.py`. There are several scripts to read the resulting dataset and print the row-count:

- `python/fastparquet_read.py`
- `python/pyarrow_read.py`
- `js/read_parquet.py`
- `golang/read_parquet.go`

In all the other languages and parquet libraries included, when reading from the parquet file's footer metadata the number of rows returned reflects only the row count from a _single chunk_ instead of the total aggregate row count. 

**It would seem that when using `fastparquet.write` with `append=True`, the `num_rows` field in the footer metadata thrift is not being correctly updated...**

Specifically, the way that `fastparquet_write.py`  is written, it will write `30` chunks of `1e5` rows each. The correct total should be `3e6`. 
