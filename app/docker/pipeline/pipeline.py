import pandas as pd
import sys  
month = sys.argv[1]

df = pd.DataFrame({"day": [1, 2], "num_passengers": [3, 4]})
df["month"] = month
print('arguments', sys.argv)

df.to_parquet(f'output_{month}.parquet')
