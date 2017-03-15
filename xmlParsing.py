import sys,zlib,base64,requests
import xml.sax.saxutils as saxutils
import xml.etree.ElementTree as ET

try:
    #Extract the file name from command-line arguement
    fileName = sys.argv[2]
    #Parse the xml content into an element tree
    tree = ET.parse(fileName)
    #Get the root of the tree
    root = tree.getroot()

    #Zipping the xml content
    if sys.argv[1]=="--gzip":
        #Get all the elements with attribute test & value 1
        for curElement in root.findall(".//*[@test='1']"):
            
            #Get the children of the element to be zipped
            curElementString = ET.tostring(curElement).split('>', 1)[1].rsplit('<', 1)[0]
            #Compress & encode the content
            curElementString=base64.b64encode(zlib.compress(curElementString))
            #Remove all the children of the element
            for curChild in list(curElement):
                curElement.remove(curChild)
            #Add the compressed content to the element text
            curElement.text=curElementString
            #Write into a file
            f=open(fileName,"w")
            tree.write(f)
            f.close()
    #Unzipping the zipped content
    elif sys.argv[1]=="--gunzip":
        #Get all the elements with attribute test & value 1
        for curElement in root.findall(".//*[@test='1']"):
            #Decode & decompress the compressed content
            curElementString=zlib.decompress(base64.b64decode(curElement.text))
            #Add the content to the text of the element
            curElement.text=curElementString
            #Write to the file
            f=open(fileName,"w")
            f.write(saxutils.unescape(ET.tostring(root)))
            f.close()
    else:
         raise NameError
    "****Bonus:Sending post request to the server****"
    tree = ET.parse(fileName)
    xml=ET.tostring(tree.getroot())
    print("sending request to http://posttestserver.com/post.php")
    print (requests.post('http://posttestserver.com/post.php', data=xml, headers={'Content-Type': 'application/xml'}).text)
except IOError:
   print("File Not Found! Please, check the file path")
except NameError:
    print("Command unknown")
    print("Input format--> python xmlParsing.py [--gunzip/gzip] [file-path]")
except zlib.error:
    print("File not compatible for compressing/de-compressing")
except  ET.ParseError:
    print("File content not supported for XML parsing")
    
       