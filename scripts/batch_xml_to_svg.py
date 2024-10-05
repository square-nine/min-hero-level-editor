#just a batch tool if you want it

import xml_to_svg #to actually get SVG files

import os #to deal with files

SOURCE = "" #use your own source file

src_xml = os.listdir(SOURCE) #get all XMLs
NUM_FILES = len(src_xml)
DESTINATION = "" #use your own destination

count = 0
for item in src_xml: #for each XML:
  xml_to_svg.XML_TO_SVG(os.path.join(SOURCE,item),item)
  print(f"done {item}") #uncomment for debug stuff
  count += 1

print("\n\nFIN")
print(f"Done {count}/{NUM_FILES}")