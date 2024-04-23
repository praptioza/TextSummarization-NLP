from PyQt5 import QtCore, QtGui, QtWidgets
from wikipediSummarization import wikipedia_page
from textSummarization import text_page
# from textSummarization import text_page

class Ui_MainWindow(object):

    def wikipedia_window(self):
        # Create window for wikipedia option start
        self.window = QtWidgets.QMainWindow()
        # Open wikipedia page GUI
        self.ui = wikipedia_page()
        self.ui.setupUi(self.window)
        self.window.show()


    def text_window(self):
        # Create window for text option for start
        self.window = QtWidgets.QMainWindow()
        # Open text page GUI
        self.ui = text_page()
        self.ui.setupUi(self.window)
        self.window.show()


    def setupUi(self, MainWindow): 
        # Main selection window
        # Create object for the current selection window
        MainWindow.setObjectName("SelectionWindow")
        MainWindow.resize(600, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # Apply Background color:
        
        # Title Label:
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(200,5,300,40))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet("QLabel {color: #AED4E6; }")
        
        # Radio button if selection open Wikipedia page
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget, clicked = lambda: self.wikipedia_window())
        self.radioButton.setGeometry(QtCore.QRect(50, 50, 300, 150))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.radioButton.setFont(font)
        self.radioButton.setStyleSheet("")
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setStyleSheet("QRadioButton {color: #F4D1AE; }")

        # Radio button if selection open text page
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget, clicked = lambda: self.text_window())
        self.radioButton_2.setGeometry(QtCore.QRect(250, 50, 300, 150))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.setStyleSheet("QRadioButton {color: #F4D1AE; }")

        # Set the text for the label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 55, 400, 55))
        self.label.setStyleSheet("QLabel {color: #F4D1AE; }")
        font = QtGui.QFont()
        font.setPointSize(1)
        font.setBold(True)
        font.setWeight(75)
        
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("SelectionWindow", "Selection Window"))
        self.radioButton.setText(_translate("SelectionWindow", "WIKIPEDIA"))
        self.radioButton_2.setText(_translate("SelectionWindow", "TEXT"))
        self.label.setText(_translate("SelectionWindow", "Please select the type of summarization you would like to perform"))
        self.titleLabel.setText(_translate("SelectionWindow", "Selection Window"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())