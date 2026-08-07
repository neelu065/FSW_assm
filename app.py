import json
import polars as pl
filename = 'housekeeping_nominal.json'

breakpoint()
abc = pl.read_json(filename)
# abc = json.loads(filename)

breakpoint()

print(abc)