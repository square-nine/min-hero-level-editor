#recompressor for the BinaryData files
import zlib #keeping the same compression tool
import os #directory scanning

#setup paths to save and read from
path_to_read = os.getcwd()
path_to_save = os.path.join(path_to_read, "recrypted")
#get all bins in reading area
allXMLs = os.listdir(path_to_read)

if "recrypted" not in allXMLs:
    os.mkdir(path_to_save)

for item in allXMLs: #for each important file
    try:
        #open as bytes and read entire file
        file = open(os.path.join(path_to_read,item), "rb").read()
        #decompress the file
        bytes = zlib.compress(file)
        #saves the file with the name it was originally
        decodedFile = open(os.path.join(path_to_save, item[:-4]+".bin"), "wb")
        decodedFile.write(bytes)
        decodedFile.close()
    except: print(f"Error in {item}")


