
from PyQt5 import QtCore, QtGui, QtWidgets
import bs4 as bs
import urllib.request
import re
import nltk
import heapq

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

class Ui_wikipedi(object):
    def summary(self):
        url = self.lineEdit.text()
        data = urllib.request.urlopen(url)
        text_read = data.read()

        parsed_text = bs.BeautifulSoup(text_read,'lxml')

        paragraphs = parsed_text.find_all('p')

        text = ""

        for p in paragraphs:
            text += p.text

        #print(metin) ## ozetlenecek metin 

        # Referans numaralarini kaldiriyoruz.
        text = re.sub(r'\[[0-9]*\]', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        print(text)

        # Seperate the sentences
        sentences = nltk.sent_tokenize(text)

        # Get the english stopwords
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

        # Get most frequent word count
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


        # Take the top 5 sentences with the highest scores.
        summary_sentences = heapq.nlargest(5, sentence_score, key=sentence_score.get)


        summary = ' '.join(summary_sentences)
        print("SUMMARY ::")
        self.textBrowser.setText(summary)
        f = open("WikiSummary.txt", "w", encoding="utf-8")
        f.write(summary)
        f.close()


    def setupUi(self, wikipedi):
        wikipedi.setObjectName("wikipedi")
        wikipedi.resize(642, 432)
        self.centralwidget = QtWidgets.QWidget(wikipedi)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.summary())
        self.pushButton.setGeometry(QtCore.QRect(540, 20, 81, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 100, 621, 291))
        self.textBrowser.setObjectName("textBrowser")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(250, 60, 131, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.label_2.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(80, 20, 391, 20))
        self.lineEdit.setObjectName("lineEdit")
        wikipedi.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(wikipedi)
        self.statusbar.setObjectName("statusbar")
        wikipedi.setStatusBar(self.statusbar)

        self.retranslateUi(wikipedi)
        QtCore.QMetaObject.connectSlotsByName(wikipedi)

    def retranslateUi(self, wikipedi):
        _translate = QtCore.QCoreApplication.translate
        wikipedi.setWindowTitle(_translate("wikipedia", "Summarizing Wikipedia Data"))
        self.label.setText(_translate("wikipedia", "URL : "))
        self.pushButton.setText(_translate("wikipedia", "Summarize"))
        self.label_2.setText(_translate("wikipedia", "Summary"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_wikipedi()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())