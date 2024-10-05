#what better way to test my code than trying to reverse-engineer an XML to an SVG?
#this might be too nuts, but would be AMAZINGG

#imports
from PIL import Image
import os
import cv2
import base64

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
      _width = abs(_width)
      #by commenting out this abs, it works perfectly. This means we need to move back the image as if we were "folding" it?
      #original formula: transform_string = f'       transform="translate({_xPos+_width/2} {_yPos+_height/2}) scale(-1 1) translate(-{_xPos+_width/2} -{_yPos+_height/2}) rotate({_rotate},{_xPos},{_yPos}) translate({_width} 0)"\n' 
      transform_string = f'       transform="matrix(-1,0,0,1,{2*_xPos},0) "\n' #accurately flips it over as above, in smaller lines. No rotation as it shouldn't be needed.

    else: transform_string = f'       transform="rotate({_rotate},{_xPos},{_yPos})"\n' #rotation only
    
    tmp_to_write = '<image\n'
    tmp_to_write +=f'       width="{_width}"\n'  #adding width
    tmp_to_write +=f'       height="{_height}"\n' #adding height
    tmp_to_write += '       preserveAspectRatio="none"\n' #other needed info
    if "imageData" in item.keys():
      tmp_to_write +=f'       xlink:href="{item["imageData"]}"\n' #image data
    else: tmp_to_write +=f'       xlink:href="{item["image"]}"\n' #image link
    tmp_to_write +=f'       id="image1-{count}"\n' #a unique ID through the count
    tmp_to_write +=  transform_string #adding transforms
    tmp_to_write +=f'       x="{_xPos}"\n'  #xPos
    tmp_to_write +=f'       y="{_yPos}"\n />' #yPos
    count += 1
    bloc += tmp_to_write
  bloc += "</g>"
  return bloc, count

def CreateWriteTextFromListV2(layer, inpList:list[dict], count=1):
  "A modified version of the above function to add the image name in the 'ID' section, for embeds. Comments for explaining are as above."
  bloc = f'<g\n     id="layer{layer}">' #now to do for structure

  for item in inpList: #these are separate to help with ordering
    _width = float(item["width"])
    _height = float(item["height"])
    _xPos = item["xPos"]
    _yPos = item["yPos"]
    _rotate = float(item["rotation"])
    _ID = item["image"][:-4] + "0"
    if "EXTEND_VIEWBOX" in selected_modes:
      _xPos += 40
      _yPos += 40
    while _ID in checklist_ID: #while the ID is in the checklist:
      if _ID not in checklist_ID: break
      _ID = _ID[:-1] + str(int(_ID[-1])+1) #increase number by one
    checklist_ID.append(_ID) #add ID to be used.
    if float(item["xScale"]) < 0: #negative x scale, so time to flip
      _width = abs(_width) #OH BRAIN
      transform_string = f'       transform="matrix(-1,0,0,1,{2*_xPos},0) "\n' #accurately flips it over as above, in smaller lines. No rotation as it shouldn't be needed.

    else: transform_string = f'       transform="rotate({_rotate},{_xPos},{_yPos})"\n' #rotation only
    tmp_to_write = '<image\n'
    tmp_to_write +=f'       width="{_width}"\n'  #adding width
    tmp_to_write +=f'       height="{_height}"\n' #adding height
    tmp_to_write += '       preserveAspectRatio="none"\n' #other needed info
    if "imageData" in item.keys(): tmp_to_write +=f'       xlink:href="{item["imageData"]}"\n' #image data
    else: tmp_to_write +=f'       xlink:href="{item["image"]}"\n' #image link
    tmp_to_write +=f'       id="{_ID}"\n' #a unique ID through the count
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

def XML_TO_SVG(XMLFile:str, XMLname:str):
  "XMl to SVG (with links). Use if you want to convert the image back into the game, and this is the default"

  #find the XML
  with open(XMLFile, "r") as file: XML_FILE = file.readlines()
  
  for item in files: 
    if item.endswith(".png"): files.remove(item)

  XML_FILE.pop() #get rid of last line (not needed, it's just a closing tag we can add later)

  #get the full dimensions
  canvas = XML_FILE[0]
  XML_FILE.pop(0) #get rid of first line now we have it
  canvas = canvas.split('="')
  full_width = float(canvas[1].removesuffix('" height'))
  full_height = float(canvas[2].removesuffix('">\n'))

  #initial bit that I need to declare as SVG
  start = f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with square_nine\'s Min Hero level editor (https://github.com/square-nine/min-hero-level-editor) -->\n\n<svg\n   width="{round(full_width*0.2645833333,2)}mm"\n   height="{round(full_height*0.2645833333,2)}mm"\n   viewBox="0 0 {round(full_width*0.2645833333,2)} {round(full_height*0.2645833333,2)}"\n   version="1.1"\n   id="svg1"\n   xml:space="preserve"\n   xmlns:xlink="http://www.w3.org/1999/xlink"\n   xmlns="http://www.w3.org/2000/svg"\n   xmlns:svg="http://www.w3.org/2000/svg"><defs\n     id="defs1" />'
  #width and height have zero effect

  #this might be good memory practice
  del full_height, full_width, canvas

  #set up places for layers. I am going to choose a "structure" layer for floor/walls,a "collision" layer for assets not normally viewed, then a "decor" layer for stuff above the floor/walls
  all_images_collisions = []
  all_images_structure = []
  all_images_decor = []

  #checklists for sprites that get added to the wrong layers.
  checkList_coll = ["collRect", "roomTransitionObject", "buttonZoneObject", "entryObject", "regularDoor"]
  checklist_structure = ["groundTile", "floorTile" "floorRunner", "Corner", "sideWall", "topWall", "bottomWall", "wallSection", "bottomDoor", "sideDoor", "topDoor"]

  for image in XML_FILE:
    #delete non-graphical stuff by avoiding them. This is solved
    if not (("music_override" in image) or ("sound3d" in image)):
      #split into tags -> nearly there
      image = image.replace('"', "")[:-3].split(" ")[3:]

      #prep as a dictionary
      curr_image_as_dict = {}
      for tag in image:
        if tag != "": propertie, value = tag.split('=') #if it's not an empty tag, create a key/value pair
        #now do different things depending on what this property is, like with locating an image
        if propertie == "spriteName": #if we have the sprite name currently, we need to process it into an image that can be found
          #if value+".png" in files: #if we can access the image already (note these images are renamed)
          curr_image_as_dict["image"] = value + ".png"

        #add the key/value pair       
        curr_image_as_dict[propertie] = value 

      #dictionary is done! process extra here
      #the scale factor -  get image dims
      img = cv2.imread(os.path.join(os.environ, curr_image_as_dict["image"]),0)
      original_height, original_width = img.shape[:2]
      #get scaled params
      height, width = undo_scaleFactors(original_height,original_width,curr_image_as_dict["xScale"], curr_image_as_dict["yScale"])
      curr_image_as_dict["height"] = str(height)
      curr_image_as_dict["width"] = str(width)
      #DON'T REMOVE SCALES - they are used to determine whether to flip or not
    
      #now to convert from pixel size to millimeters
      curr_image_as_dict["xPos"] = round(float(curr_image_as_dict["xPos"])*0.2645833333,5)
      curr_image_as_dict["yPos"] = round(float(curr_image_as_dict["yPos"])*0.2645833333,5)
      
      added = False
      #now I need to decide the layer the image is added to based on it's type
      for item in checkList_coll:
        if item in curr_image_as_dict["spriteName"]: #if it's a collision sprite
          all_images_collisions.append(curr_image_as_dict)
          added = True
      for item in checklist_structure: #add for structure
        if item in curr_image_as_dict["spriteName"]: #if it's a collision sprite
          if "_crack" in curr_image_as_dict["spriteName"]: #if it's the crack decor which will get flagged
            all_images_decor.append(curr_image_as_dict)
            added = True
          else:
            all_images_structure.append(curr_image_as_dict)
            added = True
      if added == False: #if it wasn't added to structure/collisions, it must be decor
        if "floorTile" in curr_image_as_dict["spriteName"]: all_images_structure.append(curr_image_as_dict) #this is annoying
        else: all_images_decor.append(curr_image_as_dict)
 
  #now that's all added to their respective list, it's time to add these layers!
  for item in all_images_decor: 
    if "floorTile" in item["spriteName"]:
      all_images_decor.remove(item)

  #now all of the ones are fully done, it's time to format in the way to add them..
  #adding all of the collision sprites as a bottom layer first
  bloc, count = CreateWriteTextFromList(3,all_images_collisions) #collisions
  start += bloc
  bloc,count = CreateWriteTextFromList(2,all_images_structure,count) #structure
  start += bloc
  bloc,count = CreateWriteTextFromList(1,all_images_decor,count) #decor
  start += bloc + "</svg>"

  with open(XMLname.replace(".xml",".svg"), "w") as file:
    file.write(start)

def XML_TO_SVG_Embed(XMLFile:str, XMLname:str):
  "XMl to SVG (with embedding). Use if you want to use the SVG as a standalone image, or use in other projects. More advanced"
  if os.path.isfile(os.path.join("D:/Min HEROOO/ultimate image creator/result2",XMLname.replace(".xml",".svg"))): return
  else: pass

  '''
  MODES! if you want a specific image style, use the following properties into the selected_modes variable
  all modes explained below:
  NO_COLL         -> Do not add the collision sprites layer
  NO_UI           -> Don't add the text boxes
  NO_CHESTS       -> don't add the chests
  ONLY_COLL       -> Only show the collision layer, just a fun thing to look at somethimes
  EXTEND_VIEWBOX  -> Sometimes the trees can be clipped from the viewport, so naturally this can be extended
  NO_NPC          -> Don't add the NPCs

  '''
  global selected_modes
  selected_modes = ["NO_COLL", "NO_UI", "NO_CHESTS","EXTEND_VIEWBOX"] #my recommended default modes for a nice image, but change it if you want when you download your own copy.

  #find the XML
  with open(XMLFile, "r") as file: XML_FILE = file.readlines()
  for item in files: 
    if item.endswith(".png"): files.remove(item)

  XML_FILE.pop() #get rid of last line (not needed, it's just a closing tag we can add later)

  #get the full dimensions
  canvas = XML_FILE[0]
  XML_FILE.pop(0) #get rid of first line now we have it
  canvas = canvas.split('="')
  viewBoxWidth = round(float(canvas[1].removesuffix('" height'))*0.2645833333,2)
  viewBoxHeight = round(float(canvas[2].removesuffix('">\n'))*0.2645833333,2)

  #initial bit that I need to declare as SVG, stuff from here will get more interesting/cursed. 
  if "EXTEND_VIEWBOX" in selected_modes: #Option to extend viewing window by 20mm to get a nicer image
    start = f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with square_nine\'s Min Hero level editor (https://github.com/square-nine/min-hero-level-editor) -->\n\n<svg\n   width="{viewBoxWidth}mm"\n   height="{viewBoxHeight}mm"\n   viewBox="0 0 {viewBoxWidth+80} {viewBoxHeight+80}"\n   version="1.1"\n   id="svg1"\n   xml:space="preserve"\n   xmlns:xlink="http://www.w3.org/1999/xlink"\n   xmlns="http://www.w3.org/2000/svg"\n   xmlns:svg="http://www.w3.org/2000/svg"><defs\n     id="defs1" />'
  else: #normal SVG declaration
    start = f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with square_nine\'s Min Hero level editor (https://github.com/square-nine/min-hero-level-editor) -->\n\n<svg\n   width="{viewBoxWidth}mm"\n   height="{viewBoxHeight}mm"\n   viewBox="0 0 {viewBoxWidth} {viewBoxHeight}"\n   version="1.1"\n   id="svg1"\n   xml:space="preserve"\n   xmlns:xlink="http://www.w3.org/1999/xlink"\n   xmlns="http://www.w3.org/2000/svg"\n   xmlns:svg="http://www.w3.org/2000/svg"><defs\n     id="defs1" />'
  
  #this might be good memory practice
  del viewBoxHeight, viewBoxWidth, canvas

  #set up places for layers. I am going to choose a "structure" layer for floor/walls,a "collision" layer for assets not normally viewed, then a "decor" layer for stuff above the floor/walls
  all_images_collisions = []
  all_images_structure = []
  all_images_decor = []

  #a checklist for any collision-only sprites, so it's easier to add stuff
  checkList_coll = ["collRect", "roomTransitionObject", "buttonZoneObject", "entryObject", "regularDoor","elevatorEntrance","expert_roomTransitionObject","telport","wallRect", "sound3D"]
  checklist_structure = ["groundTile", "floorTile" "floorRunner", "Corner", "sideWall", "topWall", "bottomWall", "wallSection"]

  #doors act a bit funny so adding this here
  checklist_decor = ["bottomDoor", "sideDoor", "topDoor"]

  #checking for IDs again
  global checklist_ID
  checklist_ID = []

  for image in XML_FILE:
    #delete non-graphical stuff by avoiding them
    if not (("music_override" in image) or ("sound3d" in image)):
      #split into tags -> nearly there
      image = image.replace('"', "")[:-3].split(" ")[3:]

      #prep as a dictionary
      curr_image_as_dict = {}
      for tag in image:
        if tag != "": propertie, value = tag.split('=') #if it's not an empty tag, create a key/value pair
        #now do different things depending on what this property is, like with locating an image
        if propertie == "spriteName": #if we have the sprite name currently, we need to process it into an image
          #time to convert to an embed
          with open(f"D:/xml_to_svg/{value}.png", "rb") as file: data = file.read()
          strPrefix = "data:image/png;base64," + str(base64.b64encode(data))[2:-1] #converts to base64 string used for embeds
          curr_image_as_dict["imageData"] = strPrefix 
          curr_image_as_dict["image"] = value + ".png"

        curr_image_as_dict[propertie] = value #add the key/value pair       

      #the scale factor -  get image dims
      img = cv2.imread(os.path.join(os.environ, curr_image_as_dict["image"]),0)
      original_height, original_width = img.shape[:2]
      #get scaled params
      height, width = undo_scaleFactors(original_height,original_width,curr_image_as_dict["xScale"], curr_image_as_dict["yScale"])
      curr_image_as_dict["height"] = str(height)
      curr_image_as_dict["width"] = str(width)
      #DON'T REMOVE SCALES - they are used to determine whether to flip or not
    
      #now to convert from pixel size to millimeters
      curr_image_as_dict["xPos"] = round(float(curr_image_as_dict["xPos"])*0.2645833333,5)
      curr_image_as_dict["yPos"] = round(float(curr_image_as_dict["yPos"])*0.2645833333,5)
      
      #now, time to overcomplicatedly filter out images

      added = False
      SKIP = False #if we skip

      #first filter: depending on mode:
      if ("NO_CHESTS" in selected_modes) and ("Chest" in curr_image_as_dict["image"]): #if the current image is a chest and we skipping them
        SKIP = True
      elif (("NO_NPC" in selected_modes) and (("Enemy" in curr_image_as_dict["image"]) or ("generalRoom_gemCombiner.png" == curr_image_as_dict["image"]) or ("generalRoom_gemSalesman.png" == curr_image_as_dict["image"]) or ("DoorGaurd" in curr_image_as_dict["image"]) or (("Wizard" in curr_image_as_dict["image"]) and not ("Medallion" in curr_image_as_dict["image"])))): #if the current image is an enemy, sage or misc NPC
        SKIP = True
      elif ("NO_UI" in selected_modes) and ("menus_speechBubble" in curr_image_as_dict["image"]): #if it's a speech bubble
        SKIP = True

  # THERE ARE A COUPLE BAD IMAGES, where for some reason they overlay badly. Because of that, there is quite a lot of code here dedicated to dealing with them
      if not SKIP: #if we are not skipping the image
        for item in checkList_coll:
          if item in curr_image_as_dict["spriteName"]: #if it's a collision sprite
            all_images_collisions.append(curr_image_as_dict)
            added = True
        for item in checklist_structure: #add for structure
          if item in curr_image_as_dict["spriteName"]: #if it's a structure sprite
            if "_crack" in curr_image_as_dict["spriteName"]: #if it's the crack decor which will get flagged
              all_images_decor.append(curr_image_as_dict)
              added = True
            else:
              all_images_structure.append(curr_image_as_dict)
              added = True
        for item in checklist_decor: #add for structure
          if item in curr_image_as_dict["spriteName"]: #if it's a special decor sprite
            all_images_decor.append(curr_image_as_dict)
            added = True
        if added == False: #if it wasn't added to structure/collisions, it must be decor
          if "floorTile" in curr_image_as_dict["spriteName"]: all_images_structure.append(curr_image_as_dict) #this is annoying
          else: all_images_decor.append(curr_image_as_dict)

  #now that's all added to their respective list, it's time to add these layers!
  for item in all_images_decor: #get rid of duplicate floor tile
    if "floorTile" in item["spriteName"]:
      all_images_decor.remove(item)

  #now all of the ones are fully done, it's time to format in the way to add them..
  #can do either no collision, only collision or normal depending on the mode
  if ("ONLY_COLL" in selected_modes) and ("NO_COLL" in selected_modes):
    raise ValueError("Can't have 'NO_COLL' and 'ONLY_COLL' as options.")
  if "ONLY_COLL" in selected_modes:
    bloc, count = CreateWriteTextFromListV2(1,all_images_collisions)
    start += bloc + "</svg>"
  elif "NO_COLL" in selected_modes:
    bloc,count = CreateWriteTextFromListV2(2,all_images_structure)
    start += bloc
    bloc,count = CreateWriteTextFromListV2(1,all_images_decor,count)
    start += bloc + "</svg>"
  else:
    bloc, count = CreateWriteTextFromListV2(3,all_images_collisions)
    start += bloc
    bloc,count = CreateWriteTextFromListV2(2,all_images_structure,count)
    start += bloc
    bloc,count = CreateWriteTextFromListV2(1,all_images_decor,count)
    start += bloc + "</svg>"
  #recommended to hard-code this, but it works if you don'y
  with open(XMLname.replace(".xml",".svg"), "w") as file: 
    file.write(start)

#find XML file:
for item in files:
  if item.endswith(".xml"):
    with open(os.path.join(os.environ,item),"r") as file:
      XML_FILE = file.readlines()
      name = item

XML_TO_SVG(XML_FILE,name) #change to XML_TO_SVG_Embed for alternate mode