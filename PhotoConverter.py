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
import threading

class MainWindow(Ui_MainWindow):
    def __init__(self,screen):
        super().__init__()
        self.setupUi(screen)
        screen.show()
        self.eventInit()

    def eventInit(self):

        self.exitButton.clicked.connect(lambda: sys.exit())

        self.configButton.clicked.connect(lambda: self.launchConfigWindow())

        self.selectCardButton.clicked.connect(lambda: self.getCardPath())

    def getCardPath(self):
        root = tkinter.Tk()
        root.withdraw()
        self.path = filedialog.askdirectory(title="Select path to CF Card")
        self.selectCardPath.setText(self.path)
        self.getCachePhotoPaths()

    def getCachePhotoPaths(self):
        cwd = os.getcwd()
        self.tempPhotoDir = os.path.join(cwd,'TEMP')
        try:
            os.mkdir(tempPhotoDir)
        except:
            pass

        for root,dirs,files in os.walk(self.path):
            for file in files:
                if file.endswith('.jpg'):
                    self.photosPath = root
                    break
        
        
        


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
        self.destinationTable.setColumnCount(4)
        self.destinationTable.setHorizontalHeaderLabels(['Destination','AutoTone?','Add Watermark?','Downscaling'])
        self.tHead = self.destinationTable.horizontalHeader()
        self.tHead.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tHead.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.tHead.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.tHead.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

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
        self.destinationTable.removeRow(self.destinationTable.currentRow())
            

    def eventInit(self):
        self.addDestinationButton.clicked.connect(lambda: self.launchDestinationWindow())
        self.createConfigButton.clicked.connect(lambda: self.createNewConfigFile())
        self.removeDestinationButton.clicked.connect(lambda: self.removeDestinationTableRow())
        self.saveSettingsButton.clicked.connect(lambda: self.saveConfigSettings())
        self.openConfigButton.clicked.connect(lambda: self.loadExistingConfig())
        self.addWatermark.clicked.connect(lambda: self.loadWatermark(isNew=True))
        self.enableWatermark.stateChanged.connect(lambda: self.loadWatermark())


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
        if isNew == True:
            path = self.getFilePath('txt')
        elif isNew == False:
            path = p.associationPath

        self.associationPathDisplay.setText(path)
        #Populating table
        self.associationPreview.clearContents()
        self.associationPreview.setRowCount(0)

        eventList = self.verifyAssociativeList(path)



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
        self.newDestination = [self.destinationPath,self.enableHistogramFix.isChecked(),self.enableWatermark.isChecked(),self.downScaleSelection.currentText()]

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
