from PyQt5 import QtCore, QtGui, QtWidgets
import bs4 as bs
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
import heapq
import re
import random
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import spacy
from collections import Counter

# Initialize NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nlp = spacy.load("en_core_web_sm")

class text_page(object):
    def extract_top_entities_with_tags(self, text, num_entities=10):
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        entity_counts = Counter(entities)
        top_entities = entity_counts.most_common(num_entities)
        # Remove duplicates while preserving order
        unique_entities = []
        seen_entities = set()
        for entity in top_entities:
            if entity[0] not in seen_entities:
                unique_entities.append(entity)
                seen_entities.add(entity[0])
        return unique_entities
    

    def plot_sentiment_distribution(self, sentences):
        sentiment_scores = [self.analyze_sentiment(sentence)['compound'] for sentence in sentences]
        plt.hist(sentiment_scores, bins=20, color='lightgreen', edgecolor='black', alpha=0.7)
        plt.title('Distribution of Sentiment Scores')
        plt.xlabel('Sentiment Score')
        plt.ylabel('Frequency')
        plt.show()




    def summary(self):
        text = self.plainTextEdit.toPlainText()
        text = self.preprocess_text(text=text)
        # Splitting the text into sentences.
        sentences = nltk.sent_tokenize(text)
        # Get english stopwords
        stopwords = nltk.corpus.stopwords.words('english')
        # Remove punctuation marks to find which word is repeated most frequently
        text_with_words = re.sub('[^a-zA-Z]', ' ', text)
        text_with_words = re.sub(r'\s+', ' ', text_with_words)
        # Keep track of word frequency
        word_frequency = self.calculate_word_frequency(words=nltk.word_tokenize(text_with_words))
        if not word_frequency:
            print("No words found in the text after removing stopwords.")
            return
        # Count of Most frequently repeated weighted word
        most_frequent = max(word_frequency.values())
        # Finally, to find the weighted frequency, as shown below, we can divide 
        # the occurrence count of all words by the frequency of the most occurring word.
        for word in word_frequency.keys():
            word_frequency[word] = (word_frequency[word]/most_frequent)
        # Iterate over the sentences extracted from the text to compute a score for each sentence based 
        # on the presence of words in the word_frequency structure
        sentence_score = self.calculate_sentence_score(sentences=sentences,word_frequency=word_frequency)
        # Take the top sentences with the highest score. We can take more depending on the value we provide.
        summary_sentence = heapq.nlargest(7, sentence_score, key=sentence_score.get)
        summary_total = ' '.join(summary_sentence)
        top_entities_with_tags = self.extract_top_entities_with_tags(summary_total)  # Ensure summary_total is passed as a string
        print("\n Top 10 most relevant entities with tags:")
        top_entities = []
        for entity, tag in top_entities_with_tags:
            print(f"{entity}: {tag}")
            top_entities.append(entity)

        # Apply sentiment analysis on the top two entities
        for entity in top_entities[:10]:
            sentiment_score = self.analyze_entity_sentiment(entity=entity,sentences=sentences)  # Pass the text associated with the entity
            print(f"Sentiment analysis for {entity[0]}: {sentiment_score}")


        
        # Create a word cloud from the summary
        self.generate_word_cloud(summary_total)
        self.plot_text_length_distribution(summary_sentence)
        self.plot_sentiment_distribution(summary_sentence)
        print("SUMMARY::")
        print(summary_total)
        self.textBrowser_2.setText(summary_total)
        with open("textSummarizationOutput.txt", "w") as f:
            f.write(summary_total)


    def __init__(self):
        self.stopwords = set(stopwords.words('english'))
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def preprocess_text(self, text):
        text = re.sub(r'\[[0-9]*\]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text

    def tokenize_words(self, text):
        return word_tokenize(text)

    def remove_stopwords(self, words):
        return [word for word in words if word.lower() not in self.stopwords]

    def calculate_word_frequency(self, words):
        word_frequency = {}
        for word in words:
            if word in word_frequency:
                word_frequency[word] += 1
            else:
                word_frequency[word] = 1
        return word_frequency

    def calculate_sentence_score(self, sentences, word_frequency):
        sentence_score = {}
        for sentence in sentences:
            for word in self.tokenize_words(sentence.lower()):
                if word in word_frequency:
                    if len(sentence.split(' ')) < 30:
                        if sentence in sentence_score:
                            sentence_score[sentence] += word_frequency[word]
                        else:
                            sentence_score[sentence] = word_frequency[word]
        return sentence_score

    def analyze_entity_sentiment(self, entity, sentences):
        # Extract the entity text from the tuple
        entity_text = entity[0]
        # Collect sentences containing the entity
        entity_sentences = [sentence for sentence in sentences if entity_text in sentence]
        # Analyze the sentiment of each sentence containing the entity
        sentiment_scores = [self.analyze_sentiment(sentence)['compound'] for sentence in entity_sentences]
        # Aggregate the sentiment scores
        aggregate_score = sum(sentiment_scores)
        # Determine if the overall discussion surrounding the entity is positive, negative, or neutral
        if aggregate_score > 0:
            return "Positive"
        elif aggregate_score < 0:
            return "Negative"
        else:
            return "Neutral"


    def analyze_sentiment(self, text):
        sentiment_score = self.sentiment_analyzer.polarity_scores(text)
        return sentiment_score

    def generate_word_cloud(self, text):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

    def plot_text_length_distribution(self, texts):
        text_lengths = [len(self.tokenize_words(text)) for text in texts]
        plt.hist(text_lengths, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
        plt.title('Distribution of Text Lengths')
        plt.xlabel('Number of Words')
        plt.ylabel('Frequency')
        plt.show()
        
    
    def setupUi(self, text):
        # style window
        text.setObjectName("text")
        text.resize(1200, 800)
        text.setStyleSheet("QMainWindow:{background-color:\"#E3FEF7\"}")

        # Create a central widget to hold other UI components
        self.centralwidget = QtWidgets.QWidget(text)
        self.centralwidget.setStyleSheet("background-color:\"#E3FEF7\"")
        self.centralwidget.setObjectName("centralwidget")

        # Create a label widget within the central widget for entering text label and style it
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(65, 166, 250, 50))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setStyleSheet("font: 800 20pt \"Times New Roman\";\n" "color: rgb(19, 93, 102);")
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")

        # Create a label widget within the central widget for text summary label and style it
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(65, 482, 250, 50))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setItalic(False)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("font: 800 20pt \"Times New Roman\";\n" "color: rgb(19, 93, 102);")
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")

        # Create a QTextBrowser widget and set the central widget as its parent to display rich text and allow user interaction like scrolling
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(350, 482, 750, 250))
        self.textBrowser_2.setStyleSheet("background-color: rgb(92, 151, 158)")
        self.textBrowser_2.setObjectName("textBrowser_2")

        # set other colors for the active states like text, button text, base, window
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.summary())
        self.pushButton.setGeometry(QtCore.QRect(940, 424, 160, 50))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 60, 67))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(227, 254, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 60, 67))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(227, 254, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(227, 254, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 60, 67, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)

        # set other colors for the active states like text, button text, base, window
        brush = QtGui.QBrush(QtGui.QColor(0, 60, 67))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(227, 254, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 60, 67))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(227, 254, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(227, 254, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 60, 67, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)

        # set other colors for the active states like text, button text, base, window
        brush = QtGui.QBrush(QtGui.QColor(0, 60, 67))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(227, 254, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 60, 67))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(227, 254, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(227, 254, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 60, 67, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.pushButton.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("font: 700 15pt \"Times New Roman\";\n" "color: rgb(0, 60, 67);")
        self.pushButton.setObjectName("pushButton")

        # Create a QPlainTextEdit widget and set the central widget as its parent
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(350, 166, 750, 250))
        self.plainTextEdit.setStyleSheet("background-color: rgb(92, 151, 158)")
        self.plainTextEdit.setObjectName("plainTextEdit")

        # Create a QLabel widget for title and set the central widget as its parent
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(350, 50, 500, 50))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(30)
        font.setItalic(False)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("font: 800 30pt \"Times New Roman\";\n" "color: rgb(0, 60, 67);")
        self.label_3.setObjectName("label_3")
        text.setCentralWidget(self.centralwidget)
        # Create a QStatusBar widget with the QMainWindow as its parent
        self.statusbar = QtWidgets.QStatusBar(text)
        self.statusbar.setObjectName("statusbar")
        text.setStatusBar(self.statusbar)

        self.retranslateUi(text) # Call the retranslateUi method to set the text content of the widgets based on the translation mechanism
        QtCore.QMetaObject.connectSlotsByName(text) # Automatically connect signals from the named objects in the text to the corresponding slots
   
    def retranslateUi(self, text):
        _translate = QtCore.QCoreApplication.translate
        text.setWindowTitle(_translate("text", "TextSummarization"))
        self.label.setText(_translate("text", "Enter Text Here: "))
        self.label_2.setText(_translate("text", "Summary of Text: "))
        self.pushButton.setText(_translate("text", "Summarize"))
        self.label_3.setText(_translate("text", "SUMMARY OF TEXT"))

# Example usage
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = text_page()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())