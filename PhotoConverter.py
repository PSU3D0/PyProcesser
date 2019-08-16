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
        self.params = self.loadConfigFile(propertiesPath)

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

    def loadConfigFile(self,propertiesPath):
        #Extracts values into dictionary
        config = configparser.ConfigParser()
        
        config.read(propertiesPath)
        
        self.params = {s:dict(config.items(s)) for s in config.sections()}
        self.associationPath = self.params['paths'].get('associationpath')
        self.watermarkPath = self.params['paths'].get('watermarkpath')
        #Event Info
        self.eventName = self.params['eventParamaters'].get('eventname')
        #Destination
        self.destinationVals = config['destinations']['paths']
        if self.destinationVals:
            self.destinationVals = ast.literal_eval(config['destinations']['paths'])
        else:
            pass
        


#Creating sections
def newConfigFile(fileName):

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
    #TODO Add Boolean config for association

    with open(fileName,'w') as f:
        config.write(f)



class ConfigScreen(Ui_configScreen):
    def __init__(self,screen):
        super().__init__()
        self.setupUi(screen)
        self.eventInit()

        #Change this based on # of Destination parameters
        #Also setting top row to actt as header
        self.destinationTable.setColumnCount(4)
        self.destinationTable.setHorizontalHeaderLabels(['Destination','Normalize Histogram?','Add Watermark?','Downscaling'])
        self.tHead = self.destinationTable.horizontalHeader()
        self.tHead.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tHead.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.tHead.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.tHead.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        
        
        
        self.refreshConfigFile(propertiesPath)
        
        
    #Keeping objects somewhat independent
    def refreshConfigFile(self,propertiesPath):
        #Extracts values into dictionary
        config = configparser.ConfigParser()
        
        config.read(propertiesPath)
        
        self.params = {s:dict(config.items(s)) for s in config.sections()}

        self.configPath = self.params['paths'].get('configfilepath')
        self.associationPath = self.params['paths'].get('associationpath')
        self.watermarkPath = self.params['paths'].get('watermarkpath')
        #Event Info
        self.eventName = self.params['eventParamaters'].get('eventname')
        #Destination
        self.destinationVals = config['destinations']['paths']
        if self.destinationVals:
            self.destinationVals = ast.literal_eval(config['destinations']['paths'])
            self.updateDestinationTable()
        else:
            pass

    def updateConfigScreen(self):
        self.associationPathDisplay.setText(self.associationPath)
        self.watermarkPathDisplay.setText(self.watermarkPath)
        self.eventName.setText(self.eventName)

    def updateDestinationTable(self):
        if self.destinationVals:
            for dstVal in self.destinationVals:
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

    def launchDestinationWindow(self):
        dstScreen.show()
        
    def addNewDestination(self):
        self.destinationTable.insertRow(self.destQuantity)
        self.destinationTable.setItem(self.destQuantity,0,self.newDst)
    
    def createNewConfigFile(self):
        root = tkinter.Tk()
        root.withdraw()
        fileName = filedialog.asksaveasfile(mode='w',defaultextension='.ini')
        n = fileName.name
        newConfigFile(n)
        appSettings(newPropertiesPath=n)
        self.configPath=n

    def saveConfigSettings(self):
        configparser.ConfigParser()
        




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

        config = configparser.ConfigParser()
        config.read(propertiesPath)

        self.destinationVals = config['destinations']['paths']
        if self.destinationVals:
            self.destinationVals = ast.literal_eval(config['destinations']['paths'])
            self.destinationVals.append(self.newDestination)
        else:
            self.destinationVals = [self.newDestination]
        config['destinations']['paths'] = str(self.destinationVals)
        with open(propertiesPath,'w') as configfile:
            config.write(configfile)

        ConfigS.refreshConfigFile(propertiesPath)

        



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


    #Initializing Windows
    

    mWindow = QtWidgets.QMainWindow()
    MainWindow(mWindow)

    cScreen = QtWidgets.QDialog()
    ConfigS = ConfigScreen(cScreen)

    dstScreen = QtWidgets.QDialog()
    addDestScreen = AddDestination(dstScreen)


    sys.exit(app.exec_())
