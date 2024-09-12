# Hello!

This is the repository that collects everything you need to begin editing levels in Min Hero!

So far, it seems to work perfectly. But - as this is still in its infancy - if you get any errors, please contact me (info at bottom) or create a Github issue here!

The guide to do it:

## Tools
First, it's recommended to have these installed:
* Inkscape (as the level editor)
* Python (to run encoder/decoder, and converter script)
* JPEXS Free Flash Decompiler (to modify the game files) ([download here](https://github.com/jindrapetrik/jpexs-decompiler))

Also, this guide assumes that you are using Windows 10/11. This has **not been tested** on other systems, but there should be workarounds.

## Process
Here is how it works:
(note that this is for a single room, for levels/multiple rooms, read the extra bit)
### Phase 1: Getting room as a useable file
* Pick the room that you want from the folder at [this link](https://github.com/square-nine/minhero-towerofsages-allfiles/tree/main/Source%20Files/decrypted_bins)
  * "Eggery" -> The Hatchery
  * "H#" -> Hallways
  * "A-G" -> Rooms in a floor
 
* Download either the `Source Code (zip)` file and extract all, or the named files in [Releases](https://github.com/square-nine/min-hero-level-editor/releases).
* Then, download all of the images in the `required_images` folder, these are the "building blocks" of the level editor, and it's adivsed to stick to them (unless you are a pro).
* Move the `xml_to_svg.py` file and the room file from step 1 to the same folder as `required_images`
* Run `xml_to_svg.py`. This can be done (if Python is installed) by opening the command prompt (right click option) and typing: `python xml_to_svg.py`, or you can use your preferred way to run Python files. There should be a file called `done.svg`.

### Phase 2: Editing
* Open up `done.svg` with Inkscape (or other SVG editing application) by right clicking on the file, then "Open With...", then "Inkscape".
* There are 3 layers in this SVG:
  *`layer1` -> A layer that stores all of the decor items (carpets, tables etc)
  *`layer2` -> A layer containing wall and floor tiles
  *`layer3` -> A layer that stores all non-visible but needed assets. This includes hitboxes, interaction ranges and triggers between rooms (like entrances)

To edit, just import new images **with the import type as "link"** into their respective layer, and scale/position/rotate to fit! A couple "pro tips" are listed below:
* Make sure to use the not-normally-visible sprites in `layer3` to add functionality. This is needed to actually enter and leave rooms, as well as provide walls and dialogues.
* If you don't know how to add something, look at other levels to see how they did it. You can just use Phase 1 to get more examples.
* To add custom images, make sure you also add the images into the game's SWF file

#### IMPORTANT: YOU *MUST* HAVE THE BELOW THINGS IN YOUR FILE
* Enough `CollRect.png` files to prevent the character to be able to move through walls
* 1 (or more) `RoomTransitionObject[#].png` and `entryObject[#].png` in your level, whose numbers/name correspond to what door they are placed near. Use numbers for internal doors between corridors and hallways, and the special names for their evident purpose

It's probably a better idea to not massively edit the utility files (except the `CollRect.png` files) within `layer3`, as modifying them has not been tested.

### Phase 3: Adding back
Now you have your edited level, it's time to add it back! (This assumes only 1 level was edited, for multiple levels read the extra bit)
* Move the `svg_to_xml.py` file to the `required_images` folder.
* Run `svg_to_xml.py` with the same method as `xml_to_svg.py`, then move the new `done.xml` file to a new folder along with `recompresor.py`.
* Run `recompresor.py`, and note the new `recrypted` folder. Within that folder you should have a `.bin` file.
* Open JPEXS Free Flash Decompiler and open the game SWF file you want to modify.
* Once opened, click on the `+` sign next to the `binaryData` section on the left-hand menu. Scroll through these files until you find the room that you edited (the filename of the file from the very first step of Phase 1). You can instead search for it by pressing `Ctrl + F` and typing the file's name
* Right click on this item and select the `Replace` option. Now, navigate to the file in the `recrypted` folder and select that `.bin` file.
* Click the "Save All" button in the top menu, and then close JPEXS

You have successfully edited a level! It's recommended to test out if it works by playing that level.
### Quick FAQ
Q: There's no music in my level!
A: Music is automatically added from floor tiles. Try using `[elementRoom]_groundTile.png` instead of one of the variants.

Q: When I interact with someone it breaks the game!
A: It hasn't been fully tested with overwriting dialogues, so for now it's best to not touch them. 

Q: I want to add my own images/functionality! How do I do that?
A: There is a way for both, but it's quite extensive. For now, just use the contact at the bottom. A guide will be added here later...

Q: I cannot enter my level!
A: You didn't add `roomTransitionObject` and `entryObject` triggers. See the IMPORTANT flag in phase 2.

Q: [insert other unforseen circumstance]!
A: Let me know! Let's solve it together!

## Additional Info
### For multiple rooms
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
I've tried my best to make this guide as easy to use and approachable as possible. If I have missed the mark, then contact me (square_nine) with the links in [my GitHub profile](https://github.com/square-nine) or by raising an issue here!
