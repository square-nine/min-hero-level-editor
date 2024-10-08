# this tool will help to process an Inkscape-exported Plain SVG into a Min-Hero compatiable XML file ready to then be encrypted for use!
# first, make sure you have all the images located in the folder, with the same name!

#COMPLETE

#NOTE: if you want to add sounds, that will need to be done manually

#imports
import os
import cv2

#functions
def get_scaleFactors(original_height, original_width, observed_height, observed_width):
    "returns the 'xScale' and 'yScale from original and scaled stats"
    yScale = round(round(float(observed_height)/float(original_height),7) * 1/0.2645833,10)
    xScale = round(round(float(observed_width)/float(original_width),7) * 1/0.2645833,10)
    return xScale, yScale
    
#get stuff
files = os.listdir(os.environ)

#constants
SVG_FILE = None

#find the SVG
for item in files:
    if ".svg" in item:
        with open(os.path.join(os.environ,item),"r") as file:
            SVG_FILE = file.readlines()
        break
    elif ".png" not in item: #if it isn't a PNG image
        files.remove(item) #get rid of it
#check if it exists
if SVG_FILE == None:
    print("SVG file not found!")

#now to process!

#make into a string
svg_string = ""
for item in SVG_FILE:
    svg_string += item.replace(" ","")

#then we split string how we want it. this splits roughly into a list of layers
svg_string = svg_string.split('id="layer')

#split into list of layers to add nicely
layers = []
layers.append(svg_string[2]) #structure
layers.append(svg_string[3]) #decor
layers.append(svg_string[1]) #collision

#some special processing to get the height + width
orig_data = svg_string[0]
#convert from millimeter to pixel dimensions
orig_data = orig_data.replace("\n","").split("<svg")[1].split("viewBox")[0].split('"')
canvas_width = float(orig_data[1][:-2]) * 3.7795275591
canvas_height = float(orig_data[3][:-2]) * 3.7795275591

del svg_string #memorie

#clean up layers
layers2 = []
for item in layers:
    layer_id = item[0] #get the layer ID
    tmp = item[1:].replace("/></g><g","").replace("\n","|").split("/><image") #split into manageable sections (newlines)
    layers2.append(tmp)

#beginning of what to write
to_write = f'<level width="{round(canvas_width,2)}" height="{round(canvas_height,2)}">\n'

#format these layers
for layer in layers2:
    #now to separate the layer into it's images
    images2 = []
    for image in layer:
        listy_image = image.replace("/></g></svg>","").replace("||","|").split("|") #get back each element of an image
        #now to use the elements of the image to create the elements for the XML
        for tag in listy_image: #for each special tag, process out unwanted tags
            if ("preserveAspectRatio=" in tag) or ('id="image' in tag) or ("" == tag): #not needed
                listy_image.remove(tag)
            if "" in listy_image: #blank entries
                listy_image.remove("")

        #now that listy_image is useable, time to set the image up as a dict
        img_as_dict = {}  
        fullSkip = False
        #for each special tag, create a key-value pair for it in the dict
        for tag in listy_image:
            try: 
                propertie, value = tag.replace('"',"").split('=') #get a property/value pair
                fullSkip = False
            except: fullSkip = True #it's probably a bad error due to invalid stuff
            if not fullSkip: #if we actually got property/value pair
                if propertie == "xlink:href": #if it's a link property, we want the filename
                    propertie = "spriteName"
                    curr_fileName = value #cache the file to access later
                    value = value[:-4]
                elif propertie == "transform" and ("rotate" in value): #if it's to rotate
                    propertie = "rotate"
                    value = value.replace(")","").split("rotate(")[1].split(",")[0]
                elif propertie == "transform" and ("matrix" in value): #if it's a reflection biz (i.e a negative scaling)
                    propertie = "flip" #property to sort it out later
                    value = True
                img_as_dict[propertie] = value #add to img_as_dict

        #let's get the scale factor now
        img = cv2.imread(os.path.join(os.environ, curr_fileName),0)
        original_height, original_width = img.shape[:2] #get image dimensions
        xScale, yScale = get_scaleFactors(original_height,original_width,img_as_dict["height"], img_as_dict["width"])
        img_as_dict["xScale"] = xScale #adding scales
        img_as_dict["yScale"] = yScale
        #get rid of the image dimensions
        img_as_dict.pop("width")
        img_as_dict.pop("height")

        #check if I need to change stuff (from line 101)
        if "flip" in img_as_dict.keys(): #if I need to flip it
            img_as_dict["xScale"] = -img_as_dict["xScale"]

        #now formatting to XML style, as a string
        img_as_needed_str = '  <levelObject spriteName="' + img_as_dict["spriteName"] + '" xPos="' + str(round(float(img_as_dict["x"])*3.7795275591,1)) + '" yPos="' + str(round(float(img_as_dict["y"])*3.7795275591,1)) + '" xScale="' + str(img_as_dict["xScale"]) + '" yScale="' + str(img_as_dict["yScale"]) + '" rotation="'
        try: img_as_needed_str += img_as_dict["rotate"] #if there's a rotate property, then add it
        except: img_as_needed_str += "0" #if not, default to zero
        to_write += img_as_needed_str + '"/>\n' #add closing tag
        
        #all done!

#now that I have each layer with their images, I need to add them into a file!

to_write += "</level>" #closing tag

#now to write to a file:
with open(os.path.join(os.environ,"done.xml"),"w") as file:
    file.write(to_write)

#all done!
#NOTE: this doesn't write to the XML in an exact order, I think. You'll have to do that I believe.

"""
alright, not actual scripting, but looking at what the XML is filtered by, I need to determine here what's needed to be in the SVG
since in the end, I want the output to be a list of dictionaries in the form: 
exampleImage = {
    "spriteName": 
    "xPos":
    "yPos":
    "xScale":
    "yScale":
    "rotation":
}

HOW TO GET ROTATION:
SVG keeps the rotation quite tricky to get, in the form of an encapuslated "transform" function.
example: transform="rotate(90)"
how to extract? Just search for 'transform="rotate', delete that prefix and then steal the numbers for use!
this works, I am just worried about how it will turn out due to the changing of it's location. Ah well, it should work out

so it turns out that flipping the image (i.e a negative scale factor) is actually a result of negative dimensions for the SVG. Which is weird but ah well.
so basically, instead of using *just* a transform element, or *just* using a negative width, it uses BOTH
so then you can do -x * -1 scale to flip it and also get a positive x value. 
so to flip:
new_x = -(original_x+width)
transform="scale(-1,1)"

okay let's type:

stuff got better.

So the complex formula I currently use to convert it properly in "xml_to_svg" can be summarised in the "matrix" transform as:
> transform="matrix(-1,0,0,1,2*xPos,0)"
so I will just use that to convert.
then here, I can just check for "matrix" and if so, do the reverse. That would normally be the inverse matrix, except no since this doesn't support matricies like that.


so, if it's name is "collRect", it belongs in the bottom visual layer, so the "collisions" layer in the SVG. That might be easier to do than try and use a special "collision" sprite for all cases, and it means that we can use creative new shapes (maybe!?)
have a 2nd layer called "objects" that has named "entryObject"s and "roomTransitionObject"s (use the original ones)


when adding to the XML file, make sure to add it in the special way. So first do the floor tiles ONLY, then do the walls, then floor decor then decor for tables
then add the collRects, roomTransitions and entryObjects

since I don't want to use the "id" tag of an image, it will be based on the actual image name 
(i.e "floorTile" places first, then etc etc.)
"""