import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

def run():
    pg_user = 'root'
    pg_pass = 'root'
    pg_host = 'pgdatabase'
    pg_db = 'ny_taxi'
    pg_port = 5432

    year = 2021
    month = 1
    chunksize = 100000
    target_table = 'yellow_taxi_trips'

    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f'{prefix}yellow_tripdata_2021-01.csv.gz'
    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

# INGESTING DATA IN CHUNKS
# df_iter là một iterator, mỗi lần gọi sẽ trả về một chunk của dataframe với kích thước chunksize đã định nghĩa
# Bản chất nó trả về 1 TextFileReader object, có thể được sử dụng để đọc dữ liệu theo từng phần (chunk) thay vì đọc toàn bộ dữ liệu vào bộ nhớ cùng một lúc.
# Cung cấp dtype để tránh việc phải đọc hết toàn bộ dữ liệu mới xác định được type dữ liệu
    df_iter = pd.read_csv(
        prefix + 'yellow_tripdata_2021-01.csv.gz',
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )

    # Lệnh chạy hoàn chỉnh
    first = True

    for df_chunk in tqdm(df_iter):

        if first:
            # Create table schema (no data)
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists="replace"
            )
            first = False
            print("Table created")

        # Insert chunk
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append"
        )


if __name__ == '__main__':
    run()



