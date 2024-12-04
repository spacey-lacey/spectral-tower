import pandas as pd
import sys


def extract_text_blocks(file_path, base_address=0):
    """
    Extract potential text blocks from a binary file and keep track of their addresses,
    filtering based on Shift JIS lead byte ranges.

    Parameters:
        file_path (str): Path to the binary file.
        base_address (int): Base address of the binary file (default 0).

    Returns:
        dict: A dictionary where keys are chunk addresses and values are Shift JIS strings.
    """
    with open(file_path, "rb") as f:
        data = f.read()

    # Split on 4 consecutive 0x00 bytes
    chunks = data.split(b"\x00\x00\x00\x00")
    text_blocks = {}

    current_address = base_address

    for chunk in chunks:
        chunk_size = len(chunk) + 4  # Add 4 for the `00 00 00 00` delimiter
        
        # Remove leading and trailing zeros
        chunk = chunk.strip(b"\x00")

        # Skip empty chunks
        if not chunk:
            current_address += chunk_size
            continue

        # Check if the first byte suggests Shift JIS text
        first_byte = chunk[0]
        if not (0x81 <= first_byte <= 0x9F or 0xE0 <= first_byte <= 0xEF):
            current_address += chunk_size
            continue

        # Check if the chunk is valid Shift JIS
        if is_valid_shift_jis(chunk):
            text_block = chunk.decode("shift_jis")
            # replace line breaks and spaces
            text_block = text_block.replace("\x00\x00", "\\n").replace("\u3000", " ")
            # save start and end addresses of text
            end_address = current_address + chunk_size - 4
            text_blocks[(current_address, end_address)] = text_block

        # Update current address
        current_address += chunk_size

    return text_blocks


def is_valid_shift_jis(data):
    """
    Check if a binary block is valid Shift JIS text.
    """
    try:
        data.decode("shift_jis")
        return True
    except UnicodeDecodeError:
        return False


if __name__ == "__main__":

    file_path = sys.argv[1]
    base_address = int(sys.argv[2], 16)

    # extract text and addresses
    text_dict = extract_text_blocks(file_path, base_address)

    # convert to pandas
    df = pd.DataFrame([{"Start int": start, "End int": end, "Text": text} for (start, end), text in text_dict.items()])

    # calculate gap from last address
    df["Gap"] = df["Start int"] - df["End int"].shift(1)

    # convert addresses to hex
    df["Start"] = df["Start int"].apply(lambda x: hex(x))
    df["End"] = df["End int"].apply(lambda x: hex(x))
    
    csv_file_name = "text_dict_" + str(hex(base_address)) + ".csv"
    df.to_csv(csv_file_name, columns=["Start", "End", "Gap", "Text"], sep="\t", index=False)
    print("Saved text to", csv_file_name)
