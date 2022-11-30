import parquet from "parquetjs";
import yargs from "yargs";

async function main(argv){
    let reader = await parquet.ParquetReader.openFile(argv.dataset_path);
    let cursor = reader.getCursor();
    console.log(`Num rows reported in dataset metadata: ${cursor.metadata.num_rows}`)
}

const y = yargs(process.argv)
const argv = y.option('dataset_path', {
    description: 'Absolute path to the dataset',
    type: 'string',
    default: '/mnt/db/datasets/00359d0a-314b-47e2-b63f-6a008015c34c/price_data.parquet'
}).argv

await main(argv) // Top-level await! Crazy. 2022; what a time to be alive...