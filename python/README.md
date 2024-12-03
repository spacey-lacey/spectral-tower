## Notes for RAM dumping
How I handled the RAM dumping, so I don't forget.

TO DO: write a python script to automate this entire process if I end up needing to do it again.

### Setup
Create virtual Python environment and install dependencies:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Run scripts from the `python` directory:
```
cd python
```

### Dumping RAM
Connect Bit Slicer to DuckStation while playing the game.  From the top bar, select "Menu" → "Dump All Memory" (unless I can make "Dump Memory Range" actually work).

These files are used to develop and test the map drawing scripts.

### Cleaning dumps
The RAM dump is several gigabytes.  We only care about the area that is rewriteable and, most importantly, is used by DuckStation.

Each dump contains the file `Binary Images Info.txt`, which indicates the paths for the RAM address ranges.  DuckStation should be at the top.  Jot down the last address used by DuckStation.

The dump filenames are formatted like
```
'(102) 0x101F54000 - 0x101F60000 rw-'
```
where 102 is the number of the file in proper order, the middle part is the address range, and `rw-` denotes the read/write permissions for that area in memory.

Delete the dump files for unneeded addresses.  So far I've been using this icky bash command:
```
find . -type f | awk -F'[() ]' '{
    if ($number > 511) print "\"" $0 "\""
}' | grep -v "Binary Images Info.txt" | xargs rm
```
where `$number` is the number of the first file _not_ used by Duckstation.
This command saves the binary info file but the deletes the huge meta-file of the entire RAM.

Then delete any remaining files for ranges that aren't writeable:
```
rm *r--* *r-x*
```

### "Normalize" addresses
If two dumps are not from the same play session, the RAM addresses probably will not line up.  The script `calculate_offsets.py` takes two binary info files, calculates the differences between corresponding addresses, and saves the resulting table as a pickled pandas dataframe.
```
python calculate_offsets.py
```
Currently the binary info file locations are hardcoded because I was lazy.

### Locate corresponding RAM locations across dumps
Here I am using the assumption that useful parts of the RAM will be split up the same way among dumps (i.e., the addresses may be offset but the range is the same).  

The script `tabulate_address_ranges.py` will loop through all of the dumps (in this case, 12), parse the hexadecimal address ranges in the filenames, and organize them in a pandas dataframe.  Each row is an area in memory and each column is a different dump.  The offsets will be used as necessary to line up the addresses between different "runs."  Address blocks that do not exist as a single file in every single dump (all 12) will be ignored.

### Locating relevant data in RAM
I would up doing this with the DuckStation memory viewer.  It highlights RAM addresses that have recently changed (or something, idk exactly what it chooses to highlight).

To find the map tile data, I paged through the memory viewer, focusing on areas with red numbers, and studied if/how they changed when I reached a new floor in the game.  This boiled down to me spending a lot of the time playing the game and checking the memory viewer.  It turns out the sequence `23 00 00 00 70 70 20 20` always immediately precedes the map.  This pattern is in a few places in mempory, but so far using the first one works fine.

# I found the tower/floor address and the "floor random seed" (idk what it is exactly, but it changes when you move floors or a boss is defeated) in a similar manner.  For this one I went through the first tower a billion times to expedite reaching new floors.
