# spectral-tower

Scripts and notes for developing my Spectral Tower "ramhack."  The features will be:
1. live minimap
2. live English translation

The project is designed to use Bit Slicer to interface with DuckStation on macOS on my personal computer.  Bit Slicer has Lua integration, and from there I can use python to analyze the contents of the game's RAM as I play.  The RAM itself is not modified.  The goal is to set up peripherals to enhance playing and recording/streaming.


## Live minimap
Currently in development.  The maps for the late-game towers are very large and empty, and I spend most of my time getting lost trying to find the exit.  The minimap should fix this.  Then I can finally complete the 10,000-floor tower!

Completed tasks:
1. Located the map in RAM
2. Ripped tiles for one terrain
3. Drafted scripts to draw map using tiles
4. Identified RAM addresses indicating current location (tower, floor)
5. Wrote live Bit Slicer script to read in the map when the floor changes

To do:
1. Add some debug variables to Bit Slicer script to view in main window
2. Incorporate map drawing into Bit Slicer script
3. Find a RAM address that represents terrain
4. Rip assets for other terrains
5. Modify script to use correct terrain for current floor


## Live English translation
This is all in the brainstorming phase.  It is a lower priority because I only need it if/when I intend to have an audience, and also because it is much more involved.  Unlike the dungeon map, text appears and disappears frequently on a given floor, so it is necessary to locate relevant "triggers" in RAM that tell us when text is onscreen.

The area in memory that represents the text must be located.  Text shows up in various places during different scenarios (menus, battles, etc.) so this is not as straightforward as the map.  Once again, the goal is to find the portion of memory that indicates what text tiles are being drawn, although this is not strictly necessary.

Then the text tiles need to be mapped to actual characters.  This may require a bit of work since the game uses kanji in addition to both kinds of kana.  Hopefully the tiles have relatively contiguous addresses, so I can use hex editing to find them all.  Dumping the RAM for the character naming screen could also be useful.

Now that I am thinking about it, if the text is encoded in Shift JIS, none of the above will be needed.  I could actually search the RAM during gameplay for characters I know are onscreen.  That would be so much easier.  There might even be a python implementation of Shift JIS.

After this, I need to write a python script that translates the raw text tile data into actual unicode characters.  Then, using Lua integration, write a script to dump text during gameplay so it can be translated.  The goal for translation is to have a static "database" of words and phrases with their translations.  For an RPG, the game actually doesn't have much text at all, so I think it's reasonable to translate it all myself.

Frequently reused text, like battle messages, will be stored separately from things like character dialogue and item descriptions.  If distinct "triggers" can be identified for different bits of text, each of those fields can have its own lookup table (like item names, enemy names, character classes).

If a translation is not found, print an error message instead and dump the text to a file.  Since I don't really intend to stream, any missing translations during gameplay can be manually added in post.

Then, of course, I'll need to write scripts to actually display the translations somewhere during gameplay, probably in a separate window.  Fun!
