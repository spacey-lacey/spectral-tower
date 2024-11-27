import re
import pickle
import pandas as pd
from pathlib import Path


# fix weird pandas view thing
pd.options.mode.copy_on_write = True

base_directory = "../dumps"
runs = [1, 2]
floors = range(1, 7) # 1-6

# same for all files
address_pattern = re.compile(r"0x([0-9A-Fa-f]+) - 0x([0-9A-Fa-f]+)")


def parse_files(directory):
    '''
    parse all file names in directory and store address ranges
    '''
    files = list(Path(directory).iterdir())
    data = []
    for file in files:
        match = address_pattern.search(file.name)
        if match:
            start, end = match.groups()
            dictionary = \
            {
                "Path": str(file),
                "Start": start,
                "End": end,
                "Start_int": int(start, 16),
                "End_int": int(end, 16)
            }
            data.append(dictionary)
    dataframe = pd.DataFrame(data)
    sorted_dataframe = dataframe.sort_values(by="Start_int").reset_index(drop=True)
    return sorted_dataframe


def adjust_addresses(dataframe, offsets):
    '''
    adjust integer address values by offsets from calculate_offsets.py
    '''
    # use a "cross join" to match start addresses to offsets
    merged_df = dataframe.merge(offsets, how="cross", suffixes=("_address", "_offset"))
    mask = (merged_df["Start_int_address"] >= merged_df["Start_int_offset"]) & (merged_df["Start_int_address"] < merged_df["End_int_offset"])
    merged_df = merged_df[mask]

    # add the offsets to the dataframe as a column
    # this also removes rows that do not fall within any of the ranges
    dataframe = dataframe.merge(merged_df[["Start_int_address", "Offset_int"]], left_on="Start_int", right_on= "Start_int_address", how="inner")

    # adjust the start/end addresses
    dataframe["Start_int"] = dataframe["Start_int"] + dataframe["Offset_int"]
    dataframe["End_int"] = dataframe["End_int"] + dataframe["Offset_int"]

    return dataframe


def get_common_addresses(dataframes_list):
    '''
    return starting addresses present in all dataframes
    '''
    addresses_list = [set(dataframe["Start_int"]) for dataframe in dataframes_list]
    common_addresses = set.intersection(*addresses_list)
    return common_addresses


def get_reduced_dataframe(dataframe, common_addresses):
    '''
    reduce and sort a dataframe based on common addresses
    '''
    reduced_dataframe = dataframe[dataframe["Start_int"].isin(common_addresses)]
    sorted_dataframe = reduced_dataframe.sort_values(by="Start_int").reset_index(drop=True)
    return sorted_dataframe


# get dataframes
directories = {run: {floor: base_directory + f"/run{run}/floor{floor}" for floor in floors} for run in runs}
dataframes = {run: {floor: parse_files(directories[run][floor]) for floor in floors} for run in runs}

# adjust ranges for run 2
pickle_name = "run1_minus_run2_offsets.pkl"
offsets = pd.read_pickle(pickle_name)
dataframes[2] = {floor: adjust_addresses(dataframes[2][floor], offsets) for floor in floors}

# reduce to common start addresses
dataframes_list = list(dataframes[1].values()) + list(dataframes[2].values())
common_addresses = get_common_addresses(dataframes_list)
for run in runs:
    dataframes[run] = {floor: get_reduced_dataframe(dataframes[run][floor], common_addresses) for floor in floors}

# sort files into dataframes
file_dataframe = dataframes[1][1][["Start_int", "End_int"]]
for run in runs:
    for floor in floors:
        file_dataframe[f"Run {run} Floor {floor}"] = dataframes[run][floor]["Path"]

# save to pickle
pickle_name = "aligned_dump_paths.pkl"
file_dataframe.to_pickle(pickle_name)
print("Saved organized paths to", pickle_name)
