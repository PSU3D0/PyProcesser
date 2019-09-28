from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QHeaderView, QTableWidgetItem
from ConverterMain import  Ui_MainWindow
from ConverterConfig import Ui_configScreen
from ConverterAddDestination import Ui_addDestination
from ProcessingUtils import ImageProcessor
#Work around for Segmentation Fault
import tkinter
from tkinter import filedialog

import ast
import os
import configparser
import sys
import shutil
import time

from converter_util import *

class MainWindow(Ui_MainWindow):
    def __init__(self,screen):
        super().__init__()
        self.setupUi(screen)
        screen.show()
        self.eventInit()
        self.photoListView.setColumnCount(6)
        self.photoListView.setHorizontalHeaderLabels(['Photo','Destination Path','Autotone','Watermark','New Name','Resize'])

        self.tHead = self.photoListView.horizontalHeader()

        #Ui Updates
        self.configFilePath.setText(p.configFilePath)
        

    def eventInit(self):

        self.exitButton.clicked.connect(lambda: sys.exit())

        self.configButton.clicked.connect(lambda: self.launchConfigWindow())

        self.selectCardButton.clicked.connect(lambda: self.getCardPath())

        self.startButton.clicked.connect(lambda: self.single_thread(p))

    #TODO Add multithreading support
    def single_thread(self,p):
        v = p.destinationVals
        srcPhotos = sorted([os.path.join(self.workingPath,x) for x in os.listdir(self.workingPath)])

        progressTotal = len(v)*len(srcPhotos)

        eventList = p.eventList
        cList,maxB = self.loadCardList(self.workingPath,eventList)
        #v = dst,autotone,watermark,rename
        '''
        Copy 'originals'
        Resize by type -> save to folders of same resize
        Params to all photos
        '''
        #Dict with resize as key and value list of destinations
        mappingDict = {}

        #Groups dst by size, resize only done once
        sizes = set([x[4] for x in v])
        for size in sizes:
            matchingDestinations = [x for x in v if size in x]
            mappingDict[size] = matchingDestinations


        progress = 0
        for key in sorted(mappingDict.keys(),reverse=True):#reverse=True guarentees originals are processed first
            destinations = mappingDict[key]
            for idx, p in enumerate(srcPhotos):
                pb = photoToBytes(p)
                if not key == 'Original':
                    width = int(key.split("x")[0])
                    pb = resizePhoto(pb,width)
                else:
                    pass

                for dst,isTone,isWatermark,isRename,size in destinations:
                    if isTone: pass
                    if isWatermark and p.isPlaceWatermark: pb = watermark_photo(pb,p.watermark_path)

                    if cList:
                        prev = 0
                        baseName = os.path.basename(p)
                        name = str([cList[i][0] for i in range(0,len(cList)-2) if idx >= cList[i][1] and idx < cList[i+1][1]])
                        renamed = self.newName(baseName,name)

                        dst = os.path.join(dst,renamed)
                        if not os.path.exists(dst):
                            bytesToPhoto(pb,os.path.join(dst,renamed))
                        else:
                            pass
                    else:
                        #TODO handle rare duplicates
                        dst = os.path.join(dst,os.path.basename(p))
                        if not os.path.exists(dst):
                            bytesToPhoto(pb,dst)
                        else:
                            pass
                progress+=1
                self.progressBar.setValue(int((progress/progressTotal)*100))




            

    def newName(self,photoName,newName):
        #Returns new photo name
        name = photoName.split(".")[0]
        name = name.split("-")[0]
        photoNum = name[::-1][:4][::-1]
        newName = '{}_{}_{}.{}'.format(newName,self.DATE_STRING,photoNum,'jpg')
        return newName
        

    def loadCardList(self,workingDir,eventList):
        #Finds card list in workingDir, then makes list with name,exposureNumber


        def matchNames(name):
        #Simply matches AssociationList with a value in EventList
            for a,b in eventList:
                if name == a:
                    return b
            return name

        cardFile = ''
        #Finding .txt file
        for file in os.listdir(workingDir):
            if file.endswith('.txt'):
                cardFile = os.path.join(workingDir,file)
                break
        if not cardFile:
            return None,None

        try:
            f = open(filePath,'r')
        except:
            self.printDebug("There was an error opening the association file")
        for line in f.readlines():
            line = line.rstrip("\n")
            try:
                a,b = line.split(self.delimeter)
                #Tests if exposure number is off
                b = int(b)
                #Prevents list from being loaded if values are mismatched
                if b < maxInt:
                    raise  ValueError
                #Matching names with numbers on association file load
                name = matchNames(a)
                if name == a:
                    self.printDebug("Warning no name found for {} at line {}".format(a,i))
                else:
                    a = name

            except ValueError:
                self.printDebug("Error, formatting is off at line {} \nPlease correct file, save, then press Enter".format(i))
                if not input():
                    return self.loadAssociationFile(filePath)
                else:
                    print("Exiting program...")
                    time.sleep(3)
                
                
            listFile.append([a,b])
            i+=1
            maxInt = b

        #B is the max exposure number. This must match # of photos in batch
        return listFile, b


    def printDebug(self,newText):
        txt = self.outputScreen.text
        self.outputScreen.setText(('%s\n%s' % (txt,newText)))



    def previewOutput(self,photoDir):
        self.photoListView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        for i in range(0,self.photoListView.columnCount()):
            self.tHead.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        #Following selection of retrival path, this populates list view with destinations of photos as well as new names
        dstLen = len(p.destinationVals)
        for photo in os.listdir(photoDir):
            rowCount = self.photoListView.rowCount()
            self.photoListView.insertRow(rowCount)

            self.photoListView.setItem(rowCount,0,QTableWidgetItem(str(photo)))
            #Populate table
            #TODO Preview Photo Rename
            for i in range(0,3):
                k = '\n'.join([str(v[i]) for v in p.destinationVals])

                self.photoListView.setItem(rowCount,i+1,QTableWidgetItem(k))
            self.photoListView.resizeRowsToContents()
                



    def cachePhotos(self,photoDir):
        #Also handles progress bar
        if p.preloadPhotos:
            tmpDir = self.getCachePhotoPaths()

            photos = sorted([os.path.join(photoDir,x) for x in os.listdir(photoDir)])
            photoCount = len(photos)

            for i, photo in enumerate(photos):
                baseName = os.path.basename(photo)
                
                newPath = os.path.join(tmpDir,baseName)
                shutil.copy2(photo,newPath)
                progress = int((i/photoCount)*100)
                self.cacheStatusBar.setValue(progress)
            self.cacheStatusBar.setValue(100)
            self.workingPath = tmpDir
        else:
            self.workingPath = photoDir
            self.cacheStatusBar.setValue(100)
        self.photoAmount.setText(str(len(os.listdir(self.workingPath))))
        self.previewOutput(self.workingPath)


    def getCardPath(self):
        root = tkinter.Tk()
        root.withdraw()
        self.path = filedialog.askdirectory(title="Select path to CF Card")
        self.selectCardPath.setText(self.path)
        self.cachePhotos(self.path)

    def getCachePhotoPaths(self):
        cwd = os.getcwd()
        tempPhotoDir = os.path.join(cwd,'TEMP')
        try:
            os.mkdir(tempPhotoDir)
        except:
            pass

        return tempPhotoDir
        

    def launchConfigWindow(self):
        cScreen.show()

    
        


#Creating sections




class ConfigScreen(Ui_configScreen):
    def __init__(self,screen):
        super().__init__()
        self.setupUi(screen)
        self.eventInit()
        #TODO Add more delimeter choices
        self.delimeter = (",")

        #Change this based on # of Destination parameters
        #Also setting top row to actt as header
        self.destinationTable.setColumnCount(5)
        self.destinationTable.setHorizontalHeaderLabels(['Destination','AutoTone?','Add Watermark?','Rename Photo?','Downscaling'])
        self.tHead = self.destinationTable.horizontalHeader()

        for i in range(0,self.destinationTable.columnCount()):
            self.tHead.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        self.updateConfigScreen()

    def warningBox(self,text):
        box = QtWidgets.QMessageBox()
        box.setIcon(QtWidgets.QMessageBox.Warning)
        box.setText(text)
        box.show()
        
    #Handles Association and Watermark path retrivals, and verifies. Dont repeat yourself!
    def getFilePath(self,ext):
        root = tkinter.Tk()
        root.withdraw()
        path = filedialog.askopenfilename(title="Select path to .{}".format(ext))
        #TODO Add support for multile image types
        if not path.endswith(ext):
            self.warningBox("Error, the following path is incorrect \n{}\nExpected {}".format(path,ext))
        else:
            return path


    def updateConfigScreen(self):
        self.associationPathDisplay.setText(p.associationPath)
        self.loadWatermark(isNew=False)
        self.eventName.setText(p.eventName)
        self.enablePhotoCache.setChecked(p.preloadPhotos)
        self.enableWatermark.setChecked(p.isPlaceWatermark)
        self.enableAssociationButton.setChecked(p.enableAssociation)
        self.updateDestinationTable()

    def updateDestinationTable(self):
        #TODO Find a better way to do this
        self.destinationTable.clearContents()
        self.destinationTable.setRowCount(0)

        if p.destinationVals:
            for dstVal in p.destinationVals:
                self.rowPos = self.destinationTable.rowCount()
                self.destinationTable.insertRow(self.rowPos)
                for i,val in enumerate(dstVal):
                    self.destinationTable.setItem(self.rowPos,i,QTableWidgetItem(str(val)))
        else:
            pass

    def removeDestinationTableRow(self):
        p.destinationVals.pop(self.destinationTable.currentRow())
        self.destinationTable.removeRow(self.destinationTable.currentRow())
            

    def eventInit(self):
        self.addDestinationButton.clicked.connect(lambda: self.launchDestinationWindow())
        self.createConfigButton.clicked.connect(lambda: self.createNewConfigFile())
        self.removeDestinationButton.clicked.connect(lambda: self.removeDestinationTableRow())
        self.saveSettingsButton.clicked.connect(lambda: self.saveConfigSettings())
        self.openConfigButton.clicked.connect(lambda: self.loadExistingConfig())
        self.addWatermark.clicked.connect(lambda: self.loadWatermark(isNew=True))

        self.enableWatermark.stateChanged.connect(lambda: self.loadWatermark())

        self.addAssociation.clicked.connect(lambda: self.loadAssociationFile(isNew=True))
        self.enableAssociationButton.stateChanged.connect(lambda: self.loadAssociationFile())

        p.enableassociation = self.enablePhotoCache.stateChanged.connect(lambda: self.enablePhotoCache.isChecked())


    def loadExistingConfig(self):
        path = filedialog.askopenfilename(title="Select Config File")
        p.loadConfigFile(path)
        self.updateConfigScreen()

    def launchDestinationWindow(self):
        dstScreen.show()
        
    def addNewDestination(self):
        self.destinationTable.insertRow(self.destQuantity)
        self.destinationTable.setItem(self.destQuantity,0,self.newDst)
    
    def createNewConfigFile(self):
        p.createNewConfigFile()

    def saveConfigSettings(self):
        #Might as well update the checkboxes here
        p.preloadPhotos = self.enablePhotoCache.isChecked()
        p.isPlaceWatermark = self.enableWatermark.isChecked()
        p.enableAssociation = self.enableAssociationButton.isChecked()

        p.updateConfigFile()
        cScreen.hide()

    #Turns into list, also verifies
    def verifyAssociativeList(self,path):
        eventList = []
        with open(path,'r') as f:
            i = 0
            try:
                for line in f.readlines():
                    line = line.rstrip("\n")
                    a,b = line.split()
                    eventList.append([a,b])
                    i+=1
            except:
                self.warningBox("Formatting Error at line {}".format(i))
        return eventList


    #If isNew is True, 'Add' Button was pushed, otherwise, loads from config file
    def loadAssociationFile(self,isNew=False):
        if self.enableAssociationButton.isChecked():

            self.associationPathDisplay.setDisabled(False)
            self.addAssociation.setDisabled(False)
            self.associationPreview.setDisabled(False)

            if isNew == True:
                path = self.getFilePath('txt')
            elif isNew == False:
                path = p.associationPath

            self.associationPathDisplay.setText(path)
            #Populating table
            self.associationPreview.clearContents()
            self.associationPreview.setRowCount(0)
            eventList = self.verifyAssociativeList(path)
            p.eventList = eventList

            for row in eventList:
                rowPos = self.associationPreview.rowCount()
                self.associationPreview.insertRow(rowPos)

                for idx,column in enumerate(row):
                    self.associationPreview.setItem(rowPos,i,QTableWidgetItem(str(val)))



        else:
            self.associationPathDisplay.setDisabled(True)
            self.addAssociation.setDisabled(True)
            self.associationPreview.setDisabled(True)



    def loadWatermark(self,isNew=False):
        if self.enableWatermark.isChecked():

            self.watermarkView.setDisabled(False)
            self.addWatermark.setDisabled(False)
            self.watermarkPathDisplay.setDisabled(False)

            if isNew == True:
                path = self.getFilePath('jpg')

            elif isNew == False:
                path = p.watermarkPath

            self.watermarkPathDisplay.setText(path)
            self.watermarkView.setPixmap(QtGui.QPixmap(path))
        else:
            self.watermarkView.setDisabled(True)
            self.addWatermark.setDisabled(True)
            self.watermarkPathDisplay.setDisabled(True)

        




class AddDestination(Ui_addDestination):
    def __init__(self,screen):
        super().__init__()
        self.setupUi(screen)
        self.eventInit()

    def eventInit(self):
        self.selectPath.clicked.connect(lambda: self.getDestinationPath())
        self.saveCancelSelection.accepted.connect(lambda: self.addDST())

    def getDestinationPath(self):
        root = tkinter.Tk()
        root.withdraw()
        self.destinationPath = filedialog.askdirectory(parent=root,title="Please select path to destination folder")
        self.destinationPathDisplay.setText(self.destinationPath)
    
    def addDST(self):
        #[path,(params)]
        self.destinationPathDisplay.clear()
        self.newDestination = [self.destinationPath,self.enableHistogramFix.isChecked(),self.enableWatermark.isChecked(),self.renamePhoto.isChecked(),self.downScaleSelection.currentText()]

        if p.destinationVals:
            p.destinationVals.append(self.newDestination)
        else:
            p.destinationVals = [self.newDestination]
        #TODO Call updateDestinationTable() within ConfigS
        ConfigS.updateDestinationTable()

        
#Simply loads config file and acts as weapper across Config window and main window
class AppParameters():
    def __init__(self):
        self.configFilePath = self.getConfigPath()

        if self.configFilePath:
            if os.path.exists(self.configFilePath):
                self.loadConfigFile(self.configFilePath)
            else:
                self.newConfigFile(self.configFilePath)
                self.loadConfigFile(self.configFilePath)
        else:
            self.createNewConfigFile()

        #Initialize variables
        self.eventList = []
            

    def createNewConfigFile(self):
            root = tkinter.Tk()
            root.withdraw()
            fileName = filedialog.asksaveasfile(mode='w',defaultextension='.ini')
            n = fileName.name
            self.saveConfigPath(fileName)
            self.configPath=n
            self.newConfigFile(self.configPath)
            self.loadConfigFile(self.configPath)


    def saveConfigPath(self,path):
        try:
            os.remove('photoConverterSettings.txt')
        except FileNotFoundError:
            pass
        with open("photoConverterSettings.txt",'a+') as f:
            f.writelines(path)


    def getConfigPath(self):
        #TODO Add support for windows registry
        try:
            import winreg
        except:
            pass

        root = tkinter.Tk()
        root.withdraw()

        with open('photoConverterSettings.txt','r+') as w:
            path = w.readlines()[0]
        return path

    def updateConfigFile(self):
        config = configparser.ConfigParser()
        config.read(self.configPath)


        config.set("destinations",'paths',str(self.destinationVals))

        config.set("paths","associationPath",self.associationPath)
        config.set("paths","waterMarkPath",self.watermarkPath)
        config.set("paths",'configFilePath',self.configPath)

        config.set('eventParamaters',"eventName",self.eventName)
        config.set('eventParamaters','isPlaceWatermark',str(self.isPlaceWatermark))
        config.set('eventParamaters','preloadPhotos',str(self.preloadPhotos))
        config.set('eventParamaters',"enableassociation",str(self.enableAssociation))
        #TODO Add Boolean config for association

        with open(self.configPath,'w') as f:
            config.write(f)

    
    def loadConfigFile(self,propertiesPath):
        #Extracts values into dictionary
        config = configparser.ConfigParser()
        
        config.read(propertiesPath)
        
        self.params = {s:dict(config.items(s)) for s in config.sections()}
        
        self.associationPath = self.params['paths'].get('associationpath')
        self.watermarkPath = self.params['paths'].get('watermarkpath')
        #Event Info
        self.eventName = self.params['eventParamaters'].get('eventname')
        self.isPlaceWatermark = ast.literal_eval(self.params['eventParamaters'].get('isplacewatermark'))
        self.preloadPhotos = ast.literal_eval(self.params['eventParamaters'].get('preloadphotos'))
        self.enableAssociation = ast.literal_eval(self.params['eventParamaters'].get('enableassociation'))

        #Destination
        self.destinationVals = config['destinations']['paths']
        if self.destinationVals:
            self.destinationVals = ast.literal_eval(config['destinations']['paths'])
        else:
            pass
        self.configPath = propertiesPath

    def newConfigFile(self,fileName):

        config = configparser.ConfigParser()
        config.read(fileName)

        config.add_section("destinations")
        config.add_section("paths")
        config.add_section("eventParamaters")

        config.set("destinations",'paths','')

        config.set("paths","associationPath",'')
        config.set("paths","waterMarkPath",'')
        config.set("paths",'configFilePath',value=fileName)

        config.set('eventParamaters',"eventName",'')
        config.set('eventParamaters','isPlaceWatermark','False')
        config.set('eventParamaters','preloadPhotos','False')
        config.set('eventParamaters',"enableassociation",'False')
        #TODO Add Boolean config for association

        with open(fileName,'w') as f:
            config.write(f)




#Sloppy I know
def appSettings(newPropertiesPath=None):
    if newPropertiesPath == None:
        #Fix crash on missing settings file
        with open("photoConverterSettings.txt",'r') as f:
            configPath = f.readlines()[0]
        return configPath
    else:
        try:
            os.remove('photoConverterSettings.txt')
        except FileNotFoundError:
            pass
        with open("photoConverterSettings.txt",'a+') as f:
            f.writelines(newPropertiesPath)
        return newPropertiesPath





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)


    #Get Path to properties file
    propertiesPath = appSettings()


    p = AppParameters()


    #Initializing Windows
    

    mWindow = QtWidgets.QMainWindow()
    MainWindow(mWindow)

    cScreen = QtWidgets.QDialog()
    ConfigS = ConfigScreen(cScreen)

    dstScreen = QtWidgets.QDialog()
    addDestScreen = AddDestination(dstScreen)


    sys.exit(app.exec_())
