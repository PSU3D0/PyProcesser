# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Converter2.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1050, 553)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(520, 390, 101, 81))
        self.startButton.setObjectName("startButton")
        self.configButton = QtWidgets.QPushButton(self.centralwidget)
        self.configButton.setGeometry(QtCore.QRect(10, 10, 89, 25))
        self.configButton.setObjectName("configButton")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(0, 480, 401, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.selectCardButton = QtWidgets.QPushButton(self.centralwidget)
        self.selectCardButton.setGeometry(QtCore.QRect(330, 130, 89, 31))
        self.selectCardButton.setCheckable(False)
        self.selectCardButton.setChecked(False)
        self.selectCardButton.setObjectName("selectCardButton")
        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(930, 390, 101, 81))
        self.exitButton.setObjectName("exitButton")
        self.PhotoLabel = QtWidgets.QLabel(self.centralwidget)
        self.PhotoLabel.setGeometry(QtCore.QRect(440, 130, 67, 17))
        self.PhotoLabel.setObjectName("PhotoLabel")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 40, 351, 71))
        font = QtGui.QFont()
        font.setPointSize(27)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.photoAmount = QtWidgets.QLabel(self.centralwidget)
        self.photoAmount.setGeometry(QtCore.QRect(440, 150, 61, 31))
        self.photoAmount.setAutoFillBackground(True)
        self.photoAmount.setFrameShape(QtWidgets.QFrame.Panel)
        self.photoAmount.setText("")
        self.photoAmount.setTextFormat(QtCore.Qt.PlainText)
        self.photoAmount.setObjectName("photoAmount")
        self.selectCardPath = QtWidgets.QLabel(self.centralwidget)
        self.selectCardPath.setGeometry(QtCore.QRect(10, 130, 311, 31))
        self.selectCardPath.setAutoFillBackground(True)
        self.selectCardPath.setFrameShape(QtWidgets.QFrame.Panel)
        self.selectCardPath.setText("")
        self.selectCardPath.setTextFormat(QtCore.Qt.PlainText)
        self.selectCardPath.setScaledContents(False)
        self.selectCardPath.setWordWrap(True)
        self.selectCardPath.setObjectName("selectCardPath")
        self.configFilePath = QtWidgets.QLabel(self.centralwidget)
        self.configFilePath.setGeometry(QtCore.QRect(120, 10, 311, 31))
        self.configFilePath.setAutoFillBackground(True)
        self.configFilePath.setFrameShape(QtWidgets.QFrame.Panel)
        self.configFilePath.setText("")
        self.configFilePath.setTextFormat(QtCore.Qt.PlainText)
        self.configFilePath.setScaledContents(False)
        self.configFilePath.setWordWrap(True)
        self.configFilePath.setObjectName("configFilePath")
        self.cacheStatusBar = QtWidgets.QProgressBar(self.centralwidget)
        self.cacheStatusBar.setGeometry(QtCore.QRect(10, 190, 311, 20))
        self.cacheStatusBar.setProperty("value", 0)
        self.cacheStatusBar.setObjectName("cacheStatusBar")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 170, 91, 17))
        self.label_2.setObjectName("label_2")
        self.photoListView = QtWidgets.QTableWidget(self.centralwidget)
        self.photoListView.setGeometry(QtCore.QRect(515, 40, 521, 341))
        self.photoListView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.photoListView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.photoListView.setObjectName("photoListView")
        self.photoListView.setColumnCount(0)
        self.photoListView.setRowCount(0)
        self.outputScreen = QtWidgets.QLabel(self.centralwidget)
        self.outputScreen.setGeometry(QtCore.QRect(0, 370, 401, 101))
        self.outputScreen.setStyleSheet("QLabel{\n"
"background: white;\n"
"}")
        self.outputScreen.setText("")
        self.outputScreen.setWordWrap(True)
        self.outputScreen.setObjectName("outputScreen")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1050, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Card Converter 9000"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.configButton.setText(_translate("MainWindow", "Open Config"))
        self.selectCardButton.setText(_translate("MainWindow", "Select Card"))
        self.exitButton.setText(_translate("MainWindow", "Exit"))
        self.PhotoLabel.setText(_translate("MainWindow", "#Photos"))
        self.label.setText(_translate("MainWindow", "Card Converter 9000"))
        self.label_2.setText(_translate("MainWindow", "Cache Status"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
