# spectral-tower

Scripts and notes for developing my Spectral Tower "ramhack."  The features will be:
1. live minimap
2. live English translation

The project is designed to use Bit Slicer to interface with DuckStation on macOS.  Bit Slicer has python integration, which can be used to analyze the contents of the game's RAM during play.  The RAM itself is not modified.  The goal is to set up peripherals to enhance playing and recording/streaming.


## Live minimap
Currently in development.  The goal is to have a (static) map displayed in a special window, which is updated upon moving to a new floor.

Completed tasks:
1. Located the map in RAM
2. Ripped tiles for one terrain
3. Drafted scripts to draw map using tiles
4. Identified RAM addresses indicating current location (tower, floor)
5. Wrote live Bit Slicer script to read and display map when the floor changes

To do:
1. Implement tkinter and saving in the Bit Slicer script
2. Find a RAM address that represents terrain
3. Rip assets for other terrains
4. Modify script to use correct terrain for current floor
5. Automatically resize and save maps with timestamps

### Setup
In `bit_slicer` there is a script that must be manually copied into a Bit Slicer file (gross, I know).

From the base directory, run the setup script:
```
./setup.sh
```
This inserts the (absolute) path to this directory to the Python path in Bit Slicer.  The Bit Slicer Python environment is sandboxed, so this is the only way to import the modules in this repo.

Copy the entire contents of `bit_slicer/mapping_interface.py` to the clipboard.

Open Bit Slicer.  A new file will open automatically.  Using the menu, select Variable → Add Variable → Script.  A template script with the value \#Edit Me! will be added to the file.

Double click on the script in the file.  A text editor window will open.  Delete the current contents and paste in the contents of `mapping_interface.py`.  Save the Bit Slicer file so you never have to do this again.


## Live English translation
Currently in development.  The goal is to create a static "database" of words and phrases with their translations, which can be queried during gameplay.

Completed tasks:
1. Located (some) text strings in RAM, encoded as Shift JIS
2. Wrote python script to parse and decode the text
3. Created CSV file to store translation

To do:
1. Translat2
2. Find RAM addresses that indicate appearance/disappearance of text boxes
3. Understand how the text pointers work and how they can be utilized to fetch the appropriate translation during gameplay
4. Create separate translation dictionaries for different kinds of text
5. Implement a live translation using the debug log
6. Check for missing translations
7. Automatically log translations with timestamps
