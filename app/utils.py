import polars as pl
from typing import BinaryIO

def parse_file_locs(file_stream: BinaryIO) -> list:
    """
    Parse scan locations from uplodaed csv file

        Parameters:
            file_stream (BinaryIO): Stream from uploaded file

        Returns:
            locations (list): Scan locations extracted from file
    
    """
    data = pl.read_csv(file_stream.read(), infer_schema_length = 10000)
    locations = data.select(pl.col("^.*Location$")).to_series().to_list()

    return locations
