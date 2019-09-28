# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ConverterDestinationAdd.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_addDestination(object):
    def setupUi(self, addDestination):
        addDestination.setObjectName("addDestination")
        addDestination.resize(400, 300)
        self.saveCancelSelection = QtWidgets.QDialogButtonBox(addDestination)
        self.saveCancelSelection.setGeometry(QtCore.QRect(50, 260, 341, 32))
        self.saveCancelSelection.setOrientation(QtCore.Qt.Horizontal)
        self.saveCancelSelection.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.saveCancelSelection.setObjectName("saveCancelSelection")
        self.label = QtWidgets.QLabel(addDestination)
        self.label.setGeometry(QtCore.QRect(40, 10, 301, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.selectPath = QtWidgets.QPushButton(addDestination)
        self.selectPath.setGeometry(QtCore.QRect(320, 50, 71, 31))
        self.selectPath.setObjectName("selectPath")
        self.enableHistogramFix = QtWidgets.QCheckBox(addDestination)
        self.enableHistogramFix.setEnabled(False)
        self.enableHistogramFix.setGeometry(QtCore.QRect(0, 150, 171, 23))
        self.enableHistogramFix.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.enableHistogramFix.setChecked(False)
        self.enableHistogramFix.setObjectName("enableHistogramFix")
        self.enableWatermark = QtWidgets.QCheckBox(addDestination)
        self.enableWatermark.setGeometry(QtCore.QRect(10, 180, 161, 23))
        self.enableWatermark.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.enableWatermark.setChecked(True)
        self.enableWatermark.setObjectName("enableWatermark")
        self.downScaleSelection = QtWidgets.QComboBox(addDestination)
        self.downScaleSelection.setGeometry(QtCore.QRect(280, 140, 86, 21))
        self.downScaleSelection.setObjectName("downScaleSelection")
        self.downScaleSelection.addItem("")
        self.downScaleSelection.addItem("")
        self.label_2 = QtWidgets.QLabel(addDestination)
        self.label_2.setGeometry(QtCore.QRect(270, 110, 111, 17))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.destinationPathDisplay = QtWidgets.QLabel(addDestination)
        self.destinationPathDisplay.setGeometry(QtCore.QRect(0, 50, 311, 31))
        self.destinationPathDisplay.setAutoFillBackground(True)
        self.destinationPathDisplay.setFrameShape(QtWidgets.QFrame.Panel)
        self.destinationPathDisplay.setText("")
        self.destinationPathDisplay.setTextFormat(QtCore.Qt.PlainText)
        self.destinationPathDisplay.setWordWrap(True)
        self.destinationPathDisplay.setObjectName("destinationPathDisplay")
        self.renamePhoto = QtWidgets.QCheckBox(addDestination)
        self.renamePhoto.setGeometry(QtCore.QRect(10, 210, 161, 23))
        self.renamePhoto.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.renamePhoto.setChecked(True)
        self.renamePhoto.setObjectName("renamePhoto")

        self.retranslateUi(addDestination)
        self.saveCancelSelection.accepted.connect(addDestination.accept)
        self.saveCancelSelection.rejected.connect(addDestination.reject)
        QtCore.QMetaObject.connectSlotsByName(addDestination)

    def retranslateUi(self, addDestination):
        _translate = QtCore.QCoreApplication.translate
        addDestination.setWindowTitle(_translate("addDestination", "Add Destination"))
        self.label.setText(_translate("addDestination", "Add new destination"))
        self.selectPath.setText(_translate("addDestination", "Select"))
        self.enableHistogramFix.setText(_translate("addDestination", "AutoTone"))
        self.enableWatermark.setText(_translate("addDestination", "Add Watermark"))
        self.downScaleSelection.setItemText(0, _translate("addDestination", "Original"))
        self.downScaleSelection.setItemText(1, _translate("addDestination", "600x400"))
        self.label_2.setText(_translate("addDestination", "Downscaling"))
        self.renamePhoto.setText(_translate("addDestination", "Rename Photos"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    addDestination = QtWidgets.QDialog()
    ui = Ui_addDestination()
    ui.setupUi(addDestination)
    addDestination.show()
    sys.exit(app.exec_())
