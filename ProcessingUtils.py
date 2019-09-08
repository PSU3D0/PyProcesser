import sys
import os
import multiprocessing
import cv2
import numpy as np
import PIL
from PIL import Image, ExifTags
from PIL.ImageOps import autocontrast
from PIL import ImageStat
import time
import shutil
import operator
from functools import reduce
import math

'''
Brightness histogram normalization to stretch contrast (e.g., Global Histogram Equalization, Adaptive Histogram Equalization, Contrast-Limited Adaptive Histogram Equalization)
Auto white balance to remove color "overcast" in an image
Optional: color saturation to make the image pop
Noise reduction/denoising by smoothening the speckle noise, but at the expense of some detail (e.g., Mean (Averaging) Filtering, Median Filtering, Wiener Filtering, Gaussian Filtering)
Sharpening to enhance edges (e.g., Wiener Filtering, Constrained Least Squares (Regularized) Filtering, Iterative Non-linear Restoration Using the Lucy-Richardson Algorithm, Blind Deconvolution Algorithm, Unsharp Filtering)

'''


class ImageProcessor():

    def __init__(self,srcPath,dstList,watermarkPath=None):
        self.srcPath = srcPath
        self.dstList = dstList
        self.watermarkPath = watermarkPath
        self.clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(32,32))


    def enhancePhoto(self,photo):
        #TODO Work on auto enhancing photo
        '''
        bgr = cv2.imread(photo)
        #Histogram normalize based on clahe
        lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
        l_plane = cv2.split(lab)
        l_plane[0] = self.clahe.apply(l_plane[0])
        lab = cv2.merge(l_plane)
        bgr = cv2.cvtColor(lab,cv2.COLOR_LAB2BGR)
        '''
        if self.enhance:
            #Contrast Enhance
            #im = PIL.Image.open(srcPhotPath).convert("RGB")
            postCon = autocontrast(photo,cutoff=1)

            '''
            #White balancing - This or Normalization
            a = np.array(postCon)
            b = a[:, :, ::-1].copy()
            result = cv2.normalize(b,None,0,255, cv2.NORM_MINMAX)
            '''
            '''
            #Contrast Stretching - https://stackoverflow.com/questions/7116113/normalize-histogram-brightness-and-contrast-of-a-set-of-images-using-python-im
            h = postCon.convert("L").histogram()
            lut = []
            for b in range(0, len(h), 256):
                # step size
                step = reduce(operator.add, h[b:b+256]) / 255
                # create equalization lookup table
                n = 0
                for i in range(256):
                    lut.append(n / step)
                    n = n + h[i+b]
            return postCon.point(lut*3)
            '''
            #Applying base modifier based on percieved brightness - https://stackoverflow.com/questions/3490727/what-are-some-methods-to-analyze-image-brightness-using-python?noredirect=1&lq=1
            stat = ImageStat.Stat(postCon)
            r,g,b = stat.rms

            print(math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2)))

        else:
            bgr = np.asarray(postCon)
            return bgr

    def equalizeHistogramPIL(self,photo):
        image = PIL.ImageOps.equalize(image)
        return image

    def watermark_photo(self,img,watermark_path):
        if self.watermark == False or self.watermarkPath == None:
            return img
        else:
            watermarkImage = Image.open(watermark_path)

            photoWidth, photoHeight = img.size
            watermarkWidth,watermarkHeight = watermarkImage.size
            position = (photoWidth-watermarkWidth,photoHeight-watermarkHeight)
            
            img.paste(watermarkImage,position,mask=watermarkImage)
            return img

    def copyPhoto(self,srcFolder,dstFolder):
        photoCheck = set(os.listdir(dstFolder))

        for file_name in os.listdir(srcFolder):
            if file_name not in photoCheck:
                fullPth = os.path.join(srcFolder,file_name)
                shutil.copy(fullPth,dstFolder)
    

    def resizePhoto(self,image,baseWidth):
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

    def copyPhotoWorker(self,srcDir,newDir):
        #Integrate renaming into copyPhotoWorker?
        photoCheck = set([os.path.join(newDir,x) for x in os.listdir(newDir)])

        photoList = sorted([os.path.join(srcDir,x) for x in os.listdir(srcDir)])
        newPhotoList = sorted([os.path.join(newDir,x) for x in os.listdir(srcDir)])
        for idx,photo in enumerate(photoList):
            if newPhotoList[idx] not in photoCheck:
                shutil.copy(photo,newPhotoList[idx])
    
    def resizePhotoWorker(self,photoDir,baseWidth):
        photoList = sorted([os.path.join(photoDir,x) for x in os.listdir(srcDir)])
        for photo in photoList:
            self.resizePhoto(photo,baseWidth)

    def singleProcess(self):
        exceptStr = 'original'
        for dstPath,self.enhance,self.watermark,resize in self.dstList:
            self.copyPhoto(self.srcPath,dstPath)
            print('Photo copy complete for {}'.format(dstPath))
            for photo in sorted([os.path.join(dstPath,x) for x in os.listdir(dstPath)]):
                #Code structured so photo is only opened and saved to once.
                print("Processing photo {}".format(photo))
                p = PIL.Image.open(photo)
                im = self.resizePhoto(p,resize)
                self.watermark_photo(im,self.watermarkPath)
                cvOut = self.enhancePhoto(im)
                #cvOut.save(photo)
                #cv2.imwrite(photo,cvOut)
            print("Resize & Enhance Complete")


    def multiProcess(self):
        pass
        



