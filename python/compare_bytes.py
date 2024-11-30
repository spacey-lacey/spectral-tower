import pickle
import pandas as pd


# fix weird pandas view thing
pd.options.mode.copy_on_write = True

runs = [1, 2]
floors = range(1, 7)


def compute_matching_ratio(file_paths):
    """
    Compare bytes across multiple binary files and compute the matching ratio.
    
    Parameters:
        file_paths (list): List of file paths to binary files.
        
    Returns:
        float: Fraction of matching bytes to total bytes.
    """
    # Open all files in binary mode
    files = [open(file_path, "rb") for file_path in file_paths]
    
    total_bytes = 0
    matching_bytes = 0
    
    try:
        # Read byte-by-byte using zip to iterate in parallel
        while True:
            # Read one byte from each file
            bytes_group = [f.read(1) for f in files]
            
            # Break if any file is at EOF
            if any(b == b"" for b in bytes_group):
                break
            
            total_bytes += 1
            
            # Check if all bytes match
            if all(b == bytes_group[0] for b in bytes_group):
                matching_bytes += 1
    finally:
        # Close all files
        for f in files:
            f.close()
    
    # Compute the matching ratio
    return matching_bytes / total_bytes if total_bytes > 0 else 0.0




# read in file
pickle_name = "aligned_dump_paths.pkl"
dataframe = pd.read_pickle(pickle_name)

# to store results
results = dataframe[["Start_int", "End_int"]]

# compare first five floors for a given run
for run in runs:
    column_name = f"Run {run} Floors 1-5"
    results[column_name] = pd.Series(dtype="float")
    for index in dataframe.index:
        file_list = [dataframe.at[index, f"Run {run} Floor {floor}"] for floor in range(1, 6)]
        results.at[index, column_name] = compute_matching_ratio(file_list)

for floor in floors:
    column_name = f"Floor {floor}"
    results[column_name] = pd.Series(dtype="float")
    for index in dataframe.index:
        file_list = [dataframe.at[index, f"Run {run} Floor {floor}"] for run in runs]
        results.at[index, column_name] = compute_matching_ratio(file_list)

print(results)
results = results[results["Floor 6"] != results["Floor 5"]]

pd.set_option("display.max_columns", None)
print(results)

# we only care about this memory range
files = dataframe.iloc[[1]]
print(files)
