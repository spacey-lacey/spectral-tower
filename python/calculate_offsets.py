import pickle
import pandas as pd
from pathlib import Path

runs = [1, 2]

info_file_name = "Binary Images Info.txt"
run_dir = {1: "run1/floor1", 2: "run2/floor1"}

# paths for files to compare
run_info_path = {run: Path(directory + "/" + info_file_name) for run, directory in run_dir.items()}

# get dataframes
columns = ["Path", "Start", "End"]
dataframes = {run: pd.read_csv(path, delim_whitespace=True, names=columns) for run, path in run_info_path.items()}

# keep only DuckStation entries
duckstation_mask = {run: dataframe["Path"].str.contains("DuckStation") for run, dataframe in dataframes.items()}
dataframes = {run: dataframe[duckstation_mask[run]] for run, dataframe in dataframes.items()}

# sort by path name
dataframes = {run: dataframe.sort_values(by="Path").reset_index(drop=True) for run, dataframe in dataframes.items()}

# convert hex numbers to integer
for column in ["Start", "End"]:
    for run in runs:
        dataframes[run][column + "_int"] = dataframes[run][column].apply(lambda x: int(x, 16))

# calculate address range length
for run in runs:
    dataframes[run]["Diff_int"] = dataframes[run]["End_int"] - dataframes[run]["Start_int"]

# check lengths for each run
same_length = (dataframes[1]["Diff_int"] == dataframes[2]["Diff_int"])
if not same_length.all():
    raise ValueError("One or more path ranges don't match between runs.")

# calculate offsets
results = dataframes[1]["Path"]
results["Offset_int"] = dataframes[1]["Start_int"] - dataframes[2]["Start_int"]
results["Offset"] = results["Offset_int"].apply(lambda x: str(hex(x)))
print(results["Offset"])

# save to pickle
