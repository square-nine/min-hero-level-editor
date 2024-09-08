#what better way to test my code than trying to reverse-engineer an XML to an SVG?
#this might be too nuts, but would be AMAZINGG

#imports
from PIL import Image
import os
import cv2

#functions

def undo_scaleFactors(original_height, original_width, xScale, yScale ):
    "returns the dimensions to be inserted in from the scale factor and the actual image"
    observed_height = round(float(yScale) * 0.2645833 * original_height,8)
    observed_width = round(float(xScale) * 0.2645833 * original_width,8)
    return observed_height, observed_width


def CreateWriteTextFromList(layer, inpList:list[dict], count=1):
  bloc = f'<g\n     id="layer{layer}">' #now to do for structure

  for item in inpList: #these are separate to help with ordering
    _width = float(item["width"])
    _height = float(item["height"])
    _xPos = item["xPos"]
    _yPos = item["yPos"]
    _rotate = float(item["rotation"])
    
    #converting negative widths - this is bad
    #turns out I can just use the scale
    
    if float(item["xScale"]) < 0: #negative x scale, so time to flip
      #print("Width triggered")
      _width = abs(_width) 
      #original formula: transform_string = f'       transform="translate({_xPos+_width/2} {_yPos+_height/2}) scale(-1 1) translate(-{_xPos+_width/2} -{_yPos+_height/2}) rotate({_rotate},{_xPos},{_yPos}) translate({_width} 0)"\n' 
      transform_string = f'       transform="matrix(-1,0,0,1,{2*_xPos+_width},0)"\n' #accurately flips it over as above, in smaller lines. No rotation as it shouldn't be needed.

    else: transform_string = f'       transform="rotate({_rotate},{_xPos},{_yPos})"\n' #rotation only
    
    tmp_to_write = '<image\n'
    tmp_to_write +=f'       width="{_width}"\n'  #adding width
    tmp_to_write +=f'       height="{_height}"\n' #adding height
    tmp_to_write += '       preserveAspectRatio="none"\n' #other needed info
    tmp_to_write +=f'       xlink:href="{item["image"]}"\n' #image link
    tmp_to_write +=f'       id="image1-{count}"\n' #a unique ID through the count
    tmp_to_write +=  transform_string #adding transforms
    tmp_to_write +=f'       x="{_xPos}"\n'  #xPos
    tmp_to_write +=f'       y="{_yPos}"\n />' #yPos
    count += 1
    bloc += tmp_to_write
  bloc += "</g>"
  return bloc, count

#get stuff - make sure ALL images are in same folder as XML and named nicely
os.environ = "D:/xml_to_svg"
files = os.listdir(os.environ)

XML_FILE = None

#find the XML
for item in files:
  if ".xml" in item:
    with open(os.path.join(os.environ,item),"r") as file:
      XML_FILE = file.readlines()
      files.remove(item) #remove XML file from consideration
    break

#check if it exists
if XML_FILE == None: raise FileNotFoundError("XML file not found!")

#check if more XML files exist
for item in files: 
  if ".xml" in item: raise FileExistsError("Too many XML files! Please make sure there's only 1 XML file in the image directory")

for item in files: 
  if item.endswith(".png"): files.remove(item)

XML_FILE.pop() #get rid of last line (not needed, it's just a closing tag we can add later)

#get the full dimensions
canvas = XML_FILE[0]
XML_FILE.pop(0) #get rid of first line now we have it
canvas = canvas.split('="')
full_width = float(canvas[1].removesuffix('" height'))
full_height = float(canvas[2].removesuffix('">\n'))



#initial bit that I need to declare as SVG, stuff from here will get more interesting/cursed
start = f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   width="{round(full_width*0.2645833333,2) }mm"\n   height="{round(full_height*0.2645833333 ,2)}mm"\n   viewBox="0 0 210 297"\n   version="1.1"\n   id="svg1"\n   xml:space="preserve"\n   xmlns:xlink="http://www.w3.org/1999/xlink"\n   xmlns="http://www.w3.org/2000/svg"\n   xmlns:svg="http://www.w3.org/2000/svg"><defs\n     id="defs1" />'
#the "width" and "height" might be VERY important so do know where they are

#this might be good memory practice
del full_height, full_width, canvas

#set up places for layers. I am going to choose a "structure" layer for floor/walls,a "collision" layer for assets not normally viewed, then a "decor" layer for stuff above the floor/walls
all_images_collisions = []
all_images_structure = []
all_images_decor = []

#a checklist for any collision-only sprites, so it's easier to add stuff
checkList_coll = ["collRect", "roomTransitionObject", "buttonZoneObject", "entryObject", "regularDoor"]
checklist_structure = ["groundTile", "floorTile" "floorRunner", "Corner", "sideWall", "topWall", "bottomWall", "wallSection", "bottomDoor", "sideDoor", "topDoor"]

#first step: filter out unwanted features using special case checking
for image in XML_FILE:
  #delete non-graphical stuff by avoiding them
  if not (("music_override" in image) or ("sound3d" in image)):
    #split into tags -> nearly there
    image = image.replace('"', "")[:-3].split(" ")[3:]

    #prep as a dictionary
    image_as_dict = {}
    for tag in image:
     if tag != "": propertie, value = tag.split('=') #if it's not an empty tag, create a key/value pair
     #now do different things depending on what this property is, like with locating an image
     if propertie == "spriteName": #if we have the sprite name currently, we need to process it into an image that can be found
      #if value+".png" in files: #if we can access the image already (note these images are renamed)
      image_as_dict["image"] = value + ".png"
      ''' not needed as I have provided alternates to compatibilitise
       else:  #now we need to consider special cases
          if "roomTransitionObject" in value:#roomTransitionObject derivatives
            image_as_dict["image"] = "roomTransitionObject.png"
          elif "wallRect" in value: #wallRect condition
            image_as_dict["image"] = "collRect.png"
          elif "regularDoor_eggery" == value:
            image_as_dict = "regularDoor.png"
          elif "entryObject" in value:
            image_as_dict["image"] = "collRect.png"
          elif "buttonZoneObject" in value:
            image_as_dict["image"] = "buttonZoneObject.png"
          else:
            raise ValueError(f"{value} has no defined image!")
        '''
     #add the key/value pair       
     image_as_dict[propertie] = value 

    #dictionary is done! process extra here
    #the scale factor -  get image dims
    img = cv2.imread(os.path.join(os.environ, image_as_dict["image"]),0)
    original_height, original_width = img.shape[:2]
    #get scaled params
    height, width = undo_scaleFactors(original_height,original_width,image_as_dict["xScale"], image_as_dict["yScale"])
    image_as_dict["height"] = str(height)
    image_as_dict["width"] = str(width)
    #DON'T REMOVE SCALES - they are used to determine whether to flip or not

    

    #now to convert from pixel size to millimeters
    image_as_dict["xPos"] = round(float(image_as_dict["xPos"])*0.2645833333,5)
    image_as_dict["yPos"] = round(float(image_as_dict["yPos"])*0.2645833333,5)
    
    added = False

    #now I need to decide the layer the image is added to based on it's type
    for item in checkList_coll:
      if item in image_as_dict["spriteName"]: #if it's a collision sprite
        all_images_collisions.append(image_as_dict)
        added = True
    for item in checklist_structure: #add for structure
      if item in image_as_dict["spriteName"]: #if it's a collision sprite
        if "_crack" in image_as_dict["spriteName"]: #if it's the crack decor which will get flagged
          all_images_decor.append(image_as_dict)
          added = True
        else:
          all_images_structure.append(image_as_dict)
          added = True
    if added == False: #if it wasn't added to structure/collisions, it must be decor
      if "floorTile" in image_as_dict["spriteName"]: all_images_structure.append(image_as_dict) #this is annoying
      else: all_images_decor.append(image_as_dict)

    
#now that's all added to their respective list, it's time to add these layers!
#first, a big print and some postprocessing

#for item in all_images_collisions: print(item)
#print()
for item in all_images_decor: 
  if "floorTile" in item["spriteName"]:
    all_images_decor.remove(item)
  #else: print(item)
#print()
#for item in all_images_structure: print(item)


#now all of the ones are fully done, it's time to format in the way to add them..
#adding all of the collision sprites as a bottom layer first

bloc, count = CreateWriteTextFromList(3,all_images_collisions) #collisions
start += bloc
bloc,count = CreateWriteTextFromList(2,all_images_structure,count) #structure
start += bloc
bloc,count = CreateWriteTextFromList(1,all_images_decor,count) #decor
start += bloc + "</svg>"



with open("done.svg", "w") as file:
  file.write(start)





"""
NOTES:

There are loads of special cases for the different items (due to subtle differences in setup, like shifting the visual X component)
BUT, since I only care for those that do not display or are very unique, they are listed here. Otherwise, it's the same as all other assets.

 roomTransitionObject (with variants _startingRoomToLobby and teleport/telport)
This accompanies all EntryObjects to specify a special transition (?)
Don't know what it does, but as it pairs with EntryObject, just make sure that they exist near enough. 
For example, there always needs to be a "roomTransitionObject_startingRoomToLobby" door right behind the EntryObject_0 for that door

 regularDoor, regularDoor_eggery
A non-visual collision sprite for the boss door (red one) and eggery door (yellow one) to prevent access there without keys

 wallRect
A non-visual, non-blocking piece that instead stops the character and reminds them to do something else, like get an egg from the hatchery or courtyard dialogue

 elevatorEntrance
A special variant of roomTransitionObject for entering the Tower selection menu

 collRect
Adds walls, so VERY IMPORTANT. Just sprinkle scaled versions of collRect for walls

 buttonZoneObject
A collision detector for objects. So far, it will detect healing obelisks and enable doors to be opened, and process interactions with NPCs.
So you **MUST** have one for any NPCs


 sound3d
A special object to do radial sound (very with distance). Basically not needed

**entryObject
Acts as a collision detector that links to other rooms, so VERY IMPORTANT
There are a few different versions:

 entryObject0_[orthogonal direction] -> Used to specify directionality, used for 1st entry
all other "entryObject0" are used for first entry into the floor, so you **MUST** have one of these.

 then we have "entryObject#" -> Used to specify a unique room to enter. For some reason, these don't match with other XML files but are instead their own pervading network. 
Basically just see what other floors do and copy their connecting hierarchy?
 expert_entryObject -> for the expert portals
 entryObject_startingRoomToLobby -> from the lobby to the Tower
 entryObject_lobbyFromEggery -> to get to the lobby from the hatchery (so only present in hatchery XML files)


 
special images:
 eggery_fireplace, "Torch"
These have a special animation that play. Personally I don't understand how it works, but considering it's the same thing for fireplace as well as the torches, I would say to literally carbon-copy what they use for it and hope it works. Avoid self-creation if possible.

 groundTile (all types)
These not only change the music, but also seems to randomly pick between a specific tile based on the floor, and a plain tile.
it's very weird, so I would recommend to sticking to the original tiles and once again, copying the heck out of it.
Does this mean you can set specific tiles? Yes you can. The only reason to use the original one is if you want to exactly have a pattern. Otherwise, just stick to this one.

 all NPCs have a special placing command, but that's for their visual avatar. Their actual dialogue box comes from elsewhere

 plantRoom_pond
A special image that uses the river splash effects to create a slightly better presentation
 
 menus_speechBubble
Adds a chat box, good if you have an NPC dialogue





very special
"music_override"
since I can either search for and delete (because there's no image)
but since it has all the other coordinates, only the name acts as a trigger. Means I could just let it happen and instead create a special placeholder image for this (i.e create a square there) and have it keep the special name
for now, it's easier to delete and then have a manual adding of it when needed, but it's nice to know.

I just need to do everything I did to convert to SVG -> XML except in reverse.

Let's theorise by editing



"""