# Hello! This is in progress

This is the repository that collects everything you need to begin editing levels in Min Hero!

So far, Phases 1-2 work fine, but the final phase is still being implemented. A GitHub release will be made with all of the working scripts on completion

But here's a rough guide anyway:

## Tools
First, it's recommended to have these installed:
* Inkscape (as the level editor)
* Python (to run encoder/decoder, and converter script)
* JPEXS Free Flash Decompiler (to modify the game files) ([download here](https://github.com/jindrapetrik/jpexs-decompiler))

## Process
Here is how it should work:
(note that this is for a single room, for levels/multiple rooms, read the extra bit
### Phase 1: Getting room as a useable file
* Pick the room that you want from the folder at [this link](https://github.com/square-nine/minhero-towerofsages-allfiles/tree/main/Source%20Files/decrypted_bins)
  * "Eggery" -> The Hatchery
  * "H#" -> Hallways
  * "A-G" -> Rooms in a floor
 
* Download all of the files in `scripts`, they will be needed to convert between a useable format and the format for Min Hero
* Then, download all of the images in the `required_images` folder, they will be needed to make sure there are valid images between files, as well as provide the useable components for level editing
* Move the `xml_to_svg.py` file and the room file from step 1 to the same folder as `required_images`
* Run `xml_to_svg.py`. This can be done (if Python is installed) by opening the command prompt (rigth click option) and typing: `python xml_to_svg.py`. There should be a file called `done.svg`.

### Phase 2: Editing
* Open up `done.svg` with Inkscape (or other SVG editing application) by right clicking on the file, then "Open With...", then "Inkscape".
* There are 3 layers in this SVG:
  *`layer1` -> A layer that stores all of the decor items (carpets, tables etc)
  *`layer2` -> A layer containing wall and floor tiles
  *`layer3` -> A layer that stores all non-visible but needed assets. This includes hitboxes, interaction ranges and triggers between rooms (like entrances)

To edit, just import new images into their respective layer, and scale/position/rotate to fit! A couple "pro tips" are listed below:
* Make sure to use the not-normally-visible sprites in `layer3` to add functionality, like collisions and interaction options
* If you don't know how to add something, look at other levels to see how they did it
* To add custom images, make sure you also add the images into the game's SWF file

### Phase 3: Adding back - CURRENTLY BROKEN
Now you have your edited level, it's time to add it back! (This assumes only 1 level was edited, for multiple levels read the extra bit)
* Move the `svg_to_xml.py` file to the `required_images` folder.
* Run `svg_to_xml.py` with the same method as `xml_to_svg.py`, then move the new `done_xml.xml` file to a new folder along with `recompresor.py`.
* Run `recompresor.py`, and note the new `recrypted` folder. Within that folder you should have a `.bin` file.
* Open JPEXS Free Flash Decompiler and open the game SWF file you want to modify.
* Once opened, click on the `+` sign next to the `binaryData` section on the left-hand menu. Scroll through these files until you find the room that you edited (the filename of the file from the very first step of Phase 1). You can instead search for it by pressing `Ctrl + F` and typing the file's name
* Right click on this item and select the `Replace` option. Now, navigate to the file in the `recrypted` folder and select that `.bin` file.
* Click the "Save All" button in the top menu, and then close JPEXS

You have successfully edited a level! It's recommended to test out if it works by playing that level.

### Extra notes: For multiple rooms
If you want to deal with multiple rooms, or a whole level, some stuff works differently.
* First, set up a folder to contain all of this level editing stuff, otherwise stuff will get messy. Move anything you downloaded from here into this folder.
* Then, follow Phase 1 all the way up to point 3. For points 4 and 5, move only 1 ".xml" file into the `required_images` folder, then run `xml_to_svg.py` as per point 5. Then rename `done.svg` to a meaningful name (like its original name). Then repeat those steps until all are now in SVG.

Editing is the same, just read Phase 2

To add back into the game, follow this modified guide:
* Move `svg_to_xml.py` into `required_images`, and create a separate folder and move `recompresor.py` into it.
* Move **1** SVG file into `required_images` and run `svg_to_xml.py`. Rename and move the `done_xml.xml` to the same folder as `recompresor.py` is.
* Repeat the above step until all SVG files are done.
* Run `recompresor.py` and all of the new XML files should be in the `recrypted` folder.
* Open JPEXS Free Flash Decompiler and open the game SWF file you want to modify.
* Once opened, click on the `+` sign next to the `binaryData` section on the left-hand menu. 
* For each converted XML file, find its original in the `binaryData` section, right click on this item and select the `Replace` option. Now, navigate to the file in the `recrypted` folder and select that `.bin` file.
* Once all of the new files have replaced the old ones, click the "Save All" button in the top menu. Then close JPEXS

## Help
Any questions? Contact me (square_nine) with the links in [my GitHub profile](https://github.com/square-nine)
