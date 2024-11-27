# spectral-tower

Scripts and notes for developing my Spectral Tower "ramhack."  The features will be:
1. live minimap
2. live English translation

The project is designed to use Bit Slicer to interface with DuckStation on macOS on my personal computer.  Bit Slicer has Lua integration, and from there I can use python to analyze the contents of the game's RAM as I play.  The RAM itself is not modified.  The goal is to set up peripherals to enhance playing and recording/streaming.


## Live minimap
Currently in development.  The maps for the late-game towers are very large and empty, and I spend most of my time getting lost trying to find the exit.  The minimap should fix this.  Then I can finally complete the 10,000-floor tower!

Development outline:
1. Locate the map in RAM (specifically, the background tiles).  I plan to tackle this by analyzing RAM dumps of the first tower.  This is a tedious process, and a lot of scripting is involved to even locate the areas of RAM that could contain the map data.
2. Translate the RAM data to the actual background tiles.  The game has several terrains, and this must be done for all of them.
3. Harvest the tiles themselves as image files I can work with.
4. Write a python script to display the tiles according to the raw RAM data.
5. Find a way to hook this in to the live game.  The RAM addresses are not always the same, so I'll need to use some kind of static header to locate them.
6. Learn how to use Lua (lol).
7. Consider adding other features like player position and chest locations.


### Setup
Create virtual Python environment and install dependencies:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Dumping RAM
Connect Bit Slicer to DuckStation while playing the game.  From the top bar, select "Menu" → "Dump All Memory" (unless I can make "Dump Memory Range" actually work).

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
TO DO: write a python script to automate this entire process if I end up needing to do it again.

### "Normalize" addresses
If two dumps are not from the same play session, the RAM addresses probably will not line up.  The script `calculate_offsets.py` takes two binary info files, calculates the differences between corresponding addresses, and saves the resulting table as a pickled pandas dataframe.
```
python calculate_offsets.py
```
Currently the binary info file locations are hardcoded because I was lazy.

### Locate corresponding RAM locations across dumps
Here I am using the assumption that useful parts of the RAM will be split up the same way among dumps (i.e., the addresses may be offset but the range is the same).  

The script `tabulate_address_ranges.py` will loop through all of the dumps (in this case, 12), parse the hexadecimal address ranges in the filenames, and organize them in a pandas dataframe.  Each row is an area in memory and each column is a different dump.  The offsets will be used as necessary to line up the addresses between different "runs."  Address blocks that do not exist as a single file in every single dump (all 12) will be ignored.

### Compare binary data to narrow down the search region
Here I take advantage of the following facts:
- The first five floors of the first dungeon are always the same.
- The sixth floor is randomly generated.
- The areas of memory we don't care about should, by and large, be consistent accross floors.
Therefore, we are pursuing areas of memory that are _different_ across all 5 tutorial floors in a given run, _identical_ between runs for each of the first five floors, and _different_ between runs for floor 6.

I have not come up with a detailed plan for how I will implement this, but one idea is to calculate the percentage of matching bytes for each file and implement some kind of threshold.  Another is to look for long sequences of matching bytes, but I don't have a good idea of _how_ long.



## Live English translation
This is all in the brainstorming phase.  It is a lower priority because I only need it if/when I intend to have an audience, and also because it is much more involved.  Unlike the dungeon map, text appears and disappears frequently on a given floor, so it is necessary to locate relevant "triggers" in RAM that tell us when text is onscreen.

The area in memory that represents the text must be located.  Text shows up in various places during different scenarios (menus, battles, etc.) so this is not as straightforward as the map.  Once again, the goal is to find the portion of memory that indicates what text tiles are being drawn, although this is not strictly necessary.

Then the text tiles need to be mapped to actual characters.  This may require a bit of work since the game uses kanji in addition to both kinds of kana.  Hopefully the tiles have relatively contiguous addresses, so I can use hex editing to find them all.  Dumping the RAM for the character naming screen could also be useful.

Now that I am thinking about it, if the text is encoded in Shift JIS, none of the above will be needed.  I could actually search the RAM during gameplay for characters I know are onscreen.  That would be so much easier.  There might even be a python implementation of Shift JIS.

After this, I need to write a python script that translates the raw text tile data into actual unicode characters.  Then, using Lua integration, write a script to dump text during gameplay so it can be translated.  The goal for translation is to have a static "database" of words and phrases with their translations.  For an RPG, the game actually doesn't have much text at all, so I think it's reasonable to translate it all myself.

Frequently reused text, like battle messages, will be stored separately from things like character dialogue and item descriptions.  If distinct "triggers" can be identified for different bits of text, each of those fields can have its own lookup table (like item names, enemy names, character classes).

If a translation is not found, print an error message instead and dump the text to a file.  Since I don't really intend to stream, any missing translations during gameplay can be manually added in post.

Then, of course, I'll need to write scripts to actually display the translations somewhere during gameplay, probably in a separate window.  Fun!
