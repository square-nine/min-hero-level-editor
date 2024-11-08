#recompressor for the BinaryData files
import zlib #keeping the same compression tool
import os #directory scanning

#setup paths to save and read from

path_to_read =  "\\".join(__file__.split("\\")[:-1])
path_to_save = os.path.join(path_to_read, "recrypted")
#get all XMLs in reading area
allXMLs = os.listdir(path_to_read)

if "recrypted" not in allXMLs:
    os.mkdir(path_to_save)

for item in allXMLs: #for each important file
    try:
        #open as bytes and read entire file
        if ".xml" in item:
            file = open(os.path.join(path_to_read,item), "rb").read()
            #decompress the file
            bytes = zlib.compress(file)
            #saves the file with the name it was originally
            where_to_save = os.path.join(path_to_save, item[:-4]+".bin")
            decodedFile = open(where_to_save, "wb")
            decodedFile.write(bytes)
            decodedFile.close()
            print(f"saved at {where_to_save}")
        else: pass
    except: print(f"Error in {item}")


