import os
import math

import shutil

import PIL
from PIL import Image






def photoToBytes(photo):
    return PIL.Image.open(photo)

def bytesToPhoto(pilPhoto,path):
    pilPhoto.save(path)





def resizePhoto(image,baseWidth):
    #The True speed killer.
    #photoResize is max size 
    if baseWidth == 'original':
        return image
    else:
        try:
            if hasattr(image, '_getexif'): # only present in JPEGs
                for orientation in ExifTags.TAGS.keys(): 
                    if ExifTags.TAGS[orientation]=='Orientation':
                        break 
                e = image._getexif()       # returns None if no EXIF data
                if e is not None:
                    exif=dict(e.items())
                    orientation = exif[orientation] 

                    if orientation == 3:   image = image.transpose(Image.ROTATE_180)
                    elif orientation == 6: image = image.transpose(Image.ROTATE_270)
                    elif orientation == 8: image = image.transpose(Image.ROTATE_90)
        except:
            pass
        # ^ Above is rotation fix
        wpercent = (baseWidth/float(image.size[0]))
        hsize = int((float(image.size[1])*float(wpercent)))
        image = image.resize((baseWidth,hsize), Image.ANTIALIAS)
        return image


def copyUtil(src,dst):
    #Requires full paths
    try:
        if not os.path.exists(dst):
            shutil.copy2(src,dst)
        else:
            #Manages the rare event of duplicate photos
            p1Size = os.path.getsize(src)
            p2Size = os.path.getsize(dst)
            if math.isclose(p1Size,p2Size,rel_tol=5):
                pass
            else:
                name = os.path.basename(src)
                dstPath = os.path.realpath(dst)    
                fixedName = name.split(".")[0]
                fixedName = fixedName + '-A' +'.jpg'
                dst = os.path.join(dstPath,fixedName)
                shutil.copy2(src,dst)
    except FileNotFoundError:
        pass

def watermark_photo(img,watermark_path):
    if watermark_path == None:
        pass
    else:
        watermarkImage = Image.open(watermark_path)

        photoWidth, photoHeight = img.size
        watermarkWidth,watermarkHeight = watermarkImage.size
        position = (photoWidth-watermarkWidth,photoHeight-watermarkHeight)
        
        img.paste(watermarkImage,position,mask=watermarkImage)
