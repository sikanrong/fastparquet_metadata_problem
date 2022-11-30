package main

import (
	"flag"
	"log"
	"os"

	"github.com/segmentio/parquet-go"
)

func check(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	dataset_path := flag.String("dataset_path", "/var/tmp/test.parquet", "Path to the parquet dataset")
	flag.Parse()

	ds_f, ds_err := os.Open(*dataset_path)
	check(ds_err)
	info, err := os.Stat(*dataset_path)
	check(err)
	pf, err := parquet.OpenFile(ds_f, info.Size())
	check(err)

	nrows := int64(pf.NumRows())

	log.Println("Dataset has this many rows: ", nrows)
}
