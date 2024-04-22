from PyQt5 import QtCore, QtGui, QtWidgets
import bs4 as bs
import urllib.request
import re
import nltk
import heapq

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

class text_page(object):
    def summary(self):
        text = self.plainTextEdit.toPlainText()
        text = re.sub(r'\[[0-9]*\]', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        print(text)

        # Splitting the text into sentences.
        sentences = nltk.sent_tokenize(text)

        # Get english stopwords
        stopwords = nltk.corpus.stopwords.words('english')

        # Remove punctuation marks to find which word is repeated most frequently
        text_with_words = re.sub('[^a-zA-Z]', ' ', text )
        text_with_words = re.sub(r'\s+', ' ', text_with_words)

        # Keep track of word frequency
        word_frequency = {}
        # If word is not a stop word we will add 1 to its count if it is present in the word_frequency
        # If not start with 1  
        for word in nltk.word_tokenize(text_with_words):
            if word not in stopwords:
                if word in word_frequency.keys():
                    word_frequency[word] += 1
                else:
                    word_frequency[word] = 1

        # Count of Most frequently repeated weighted word
        most_frequent = max(word_frequency.values())

        # Finally, to find the weighted frequency, as shown below, we can divide 
        # the occurrence count of all words by the frequency of the most occurring word.
        for word in word_frequency.keys():
            word_frequency[word] = (word_frequency[word]/most_frequent)

        # Iterate over the sentences extracted from the text to compute a score for each sentence based 
        # on the presence of words in the word_frequency structure
        sentence_score = {}
        for sentence in sentences:
            for word in nltk.word_tokenize(sentence.lower()):
                if word in word_frequency.keys():
                    if len(sentence.split(' ')) < 30: # Calculate scores for sentences with fewer than 30 words to avoid excessive length
                        if sentence in sentence_score.keys(): # The frequency of the first word in the sentence is assigned
                            sentence_score[sentence] += word_frequency[word]
                        else:
                            sentence_score[sentence] = word_frequency[word]


        # Take the top sentences with the highest score. We can take more depending on the value we provide.
        summary_sentence = heapq.nlargest(7, sentence_score, key=sentence_score.get)

        summary_total = ' '.join(summary_sentence)
        print("SUMMARY::")
        print(summary_total)
        self.textBrowser_2.setText(summary_total)
        f = open("textSummarizationOutput.txt", "w")
        f.write(summary_total)
        f.close()

        
    def setupUi(self, text):
        text.setObjectName("text")
        text.resize(697, 584)
        self.centralwidget = QtWidgets.QWidget(text)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 89, 181, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 400, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(200, 290, 481, 251))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.summary())
        self.pushButton.setGeometry(QtCore.QRect(20, 250, 151, 51))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.pushButton.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(200, 10, 481, 251))
        self.plainTextEdit.setObjectName("plainTextEdit")
        text.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(text)
        self.statusbar.setObjectName("statusbar")
        text.setStatusBar(self.statusbar)

        self.retranslateUi(text)
        QtCore.QMetaObject.connectSlotsByName(text)

    def retranslateUi(self, text):
        _translate = QtCore.QCoreApplication.translate
        text.setWindowTitle(_translate("text", "TextSummarization"))
        self.label.setText(_translate("text", "Text"))
        self.label_2.setText(_translate("text", "Summary"))
        self.pushButton.setText(_translate("text", "Summarize"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = text_page()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())