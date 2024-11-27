import re
import pickle
import pandas as pd
from pathlib import Path

runs = [1, 2]
floors = range(1, 7) # 1-6

# same for all files
address_pattern = re.compile(r"0x([0-9A-Fa-f]+) - 0x([0-9A-Fa-f]+)")

# Function to parse file names and extract ranges
def parse_files(directory):
    files = list(Path(directory).iterdir())
    data = []


    for file in files:
        match = address_pattern.search(file.name)
        if match:
            start, end = match.groups()
            data.append({
                "Path": str(file),
                "Start": int(start, 16),
                "End": int(end, 16)
            })
    return pd.DataFrame(data)



# table
# one run at a time
# one dataframe for each floor

# file name, start address, end address
