import pickle
import pandas as pd


floors = range(1, 7)
runs = range(1, 3)


def find_common_zero_sequences(file_paths, min_zero_length=64):
    """
    Find common zero-byte sequences across multiple binary files.

    Parameters:
        file_paths (list): List of file paths to binary files.
        min_zero_length (int): Minimum length of consecutive zeros to consider as a separator.

    Returns:
        list: A list of tuples (start_position, end_position) for common zero-byte sequences.
    """
    files = [open(file_path, "rb") for file_path in file_paths]
    common_zero_sequences = []
    current_start = None
    pos = 0

    try:
        while True:
            # Read one byte from each file
            bytes_group = [f.read(1) for f in files]

            # Stop if any file reaches EOF
            if any(b == b"" for b in bytes_group):
                break

            # Check if all files have zero bytes at this position
            if all(b == b"\x00" for b in bytes_group):
                if current_start is None:
                    current_start = pos  # Start a new zero-byte sequence
            else:
                # If zero-byte sequence ends, check its length
                if current_start is not None:
                    length = pos - current_start
                    if length >= min_zero_length:
                        common_zero_sequences.append((current_start, pos))
                    current_start = None  # Reset sequence
            pos += 1

        # Handle sequence at EOF
        if current_start is not None and pos - current_start >= min_zero_length:
            common_zero_sequences.append((current_start, pos))

    finally:
        for f in files:
            f.close()

    return common_zero_sequences



def extract_chunks_from_files(file_paths, zero_sequences):
    """
    Extract chunks from multiple binary files based on common zero-byte sequences.

    Parameters:
        file_paths (list): List of file paths to binary files.
        zero_sequences (list): List of tuples (start, end) for zero-byte sequences.

    Returns:
        dict: A dictionary where each key is a file path, and the value is a list of chunks.
    """
    chunks = {file_path: [] for file_path in file_paths}

    for file_path in file_paths:
        with open(file_path, "rb") as f:
            prev_end = 0  # Start of the first chunk
            for start, end in zero_sequences:
                # Read the chunk between the previous end and the current zero sequence start
                f.seek(prev_end)
                chunk_data = f.read(start - prev_end)
                chunks[file_path].append({"start": prev_end, "end": start, "data": chunk_data})
                prev_end = end  # Move to the end of the zero sequence

            # Handle the final chunk after the last zero sequence
            f.seek(prev_end)
            chunk_data = f.read()
            chunks[file_path].append({"start": prev_end, "end": None, "data": chunk_data})

    return chunks


def compute_matching_ratio_per_chunk(chunks_dict):
    """
    Compare bytes in each chunk across multiple binary files and compute the matching ratio per chunk.

    Parameters:
        chunks_dict (dict): A dictionary where keys are file paths, and values are lists of chunks.
                           Each chunk is a dict with keys: "start", "end", "data".

    Returns:
        list: A list of dictionaries, where each entry corresponds to a chunk and contains:
              - 'chunk_index': Index of the chunk.
              - 'matching_bytes': Number of matching bytes in the chunk.
              - 'total_bytes': Total number of bytes in the chunk.
              - 'matching_ratio': Fraction of matching bytes in the chunk.
    """
    # Ensure all files have the same number of chunks
    num_chunks = len(next(iter(chunks_dict.values())))  # Get number of chunks from the first file
    for file_path, file_chunks in chunks_dict.items():
        if len(file_chunks) != num_chunks:
            raise ValueError(f"File {file_path} has a different number of chunks ({len(file_chunks)}) than others ({num_chunks}).")

    chunk_results = []

    # Iterate through corresponding chunks
    for chunk_index in range(num_chunks):
        # Get the chunk data for all files at the current index
        chunk_data_list = [chunks_dict[file_path][chunk_index]["data"] for file_path in chunks_dict]

        # Ensure all chunks are the same length
        chunk_lengths = [len(chunk_data) for chunk_data in chunk_data_list]
        if len(set(chunk_lengths)) != 1:
            raise ValueError(f"Chunks at index {chunk_index} have different lengths: {chunk_lengths}")

        # Compare bytes within this chunk
        total_bytes = chunk_lengths[0]  # Length of the chunk (all are the same)
        matching_bytes = 0

        for i in range(total_bytes):  # Iterate byte by byte
            if all(chunk_data[i] == chunk_data_list[0][i] for chunk_data in chunk_data_list):
                matching_bytes += 1

        # Compute matching ratio for this chunk
        matching_ratio = matching_bytes / total_bytes if total_bytes > 0 else 0.0

        # Store results
        chunk_results.append({
            "chunk_index": chunk_index,
            "matching_bytes": matching_bytes,
            "total_bytes": total_bytes,
            "matching_ratio": matching_ratio
        })

    return chunk_results



# read in file
pickle_name = "aligned_dump_paths.pkl"
dataframe = pd.read_pickle(pickle_name)
file_paths = [dataframe.at[1, column] for column in dataframe.columns if "Floor" in column]
print(file_paths)

# Step 1: Find common zero-byte sequences
common_zero_sequences = find_common_zero_sequences(file_paths, min_zero_length=2000)

# Step 2: Extract chunks from each file
chunks = extract_chunks_from_files(file_paths, common_zero_sequences)

# Compute the matching ratio per chunk
for floor in floors:
    floor_chunks = {}
    print("floor" + str(floor))
    for key in chunks.keys():
        if f"floor{floor}" in key:
            floor_chunks[key] = chunks[key]

    chunk_results = compute_matching_ratio_per_chunk(floor_chunks)

# Print the results
    for result in chunk_results:
        print(f"Chunk {result['chunk_index']}: Matching Bytes = {result['matching_bytes']}, "
              f"Total Bytes = {result['total_bytes']}, Matching Ratio = {result['matching_ratio']:.2%}")

# Compute the matching ratio per chunk
for run in runs:
    run_chunks = {}
    print("run" + str(run))
    for key in chunks.keys():
        if f"run{run}" in key:
            run_chunks[key] = chunks[key]

    chunk_results = compute_matching_ratio_per_chunk(floor_chunks)

# Print the results
    for result in chunk_results:
        print(f"Chunk {result['chunk_index']}: Matching Bytes = {result['matching_bytes']}, "
              f"Total Bytes = {result['total_bytes']}, Matching Ratio = {result['matching_ratio']:.2%}")
