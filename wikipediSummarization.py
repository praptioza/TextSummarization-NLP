from PyQt5 import QtCore, QtGui, QtWidgets
import bs4 as bs
import urllib.request
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
from nltk.util import bigrams


# Initialize NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
nlp = spacy.load("en_core_web_sm")

class wikipedia_page(object):

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
        url = self.lineEdit.text()
        data = urllib.request.urlopen(url)
        text_read = data.read()

        parsed_text = bs.BeautifulSoup(text_read,'lxml')

        paragraphs = parsed_text.find_all('p')

        text = ""

        for p in paragraphs:
            text += p.text

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
        top_entities_with_tags = self.extract_top_entities_with_tags(text_with_words)  # Ensure summary_total is passed as a string
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
        self.textBrowser.setText(summary_total)
        with open("wikipediaSummarizationOutput.txt", "w") as f:
            f.write(summary_total)

        # New Data Visualizations
        self.show_wordcloud(text)
        self.show_top_10_words(text)
        self.show_bigrams(text)
        self.show_class_distribution(text)
        self.show_text_avg_length(text)
        self.show_sentiment_polarity(sentences)
        
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
        text_lengths = [len(self.tokenize_words(text

)) for text in texts]
        plt.hist(text_lengths, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
        plt.title('Distribution of Text Lengths')
        plt.xlabel('Number of Words')
        plt.ylabel('Frequency')
        plt.show()
        
    def show_wordcloud(self, text):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud')
        plt.show()

    def show_top_10_words(self, text):
        words = nltk.word_tokenize(text)
        word_freq = nltk.FreqDist(words)
        plt.figure(figsize=(10, 5))
        word_freq.plot(10, cumulative=False)
        plt.title('Top 10 Words')
        plt.show()

    def show_bigrams(self, text):
        words = nltk.word_tokenize(text)
        bigram_freq = nltk.FreqDist(list(bigrams(words)))
        plt.figure(figsize=(10, 5))
        bigram_freq.plot(10, cumulative=False)
        plt.title('Top 10 Bigrams')
        plt.show()

    def show_class_distribution(self, text):
        # You need to implement this based on your data classes
        classes = re.findall(r'\b\w+\b', text)
        class_counter = Counter(classes)
        plt.bar(class_counter.keys(), class_counter.values(), color='lightcoral')
        plt.title('Class Distribution')
        plt.xlabel('Classes')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.show()

    def show_text_avg_length(self, text):
        sentences = nltk.sent_tokenize(text)
        avg_length = sum(len(sent.split()) for sent in sentences) / len(sentences)
        plt.bar(["Average Text Length"], [avg_length], color='lightblue')
        plt.title('Average Text Length')
        plt.ylabel('Number of Words')
        plt.show()

    def show_sentiment_polarity(self, sentences):
        sentiment_scores = [self.analyze_sentiment(sentence)['compound'] for sentence in sentences]
        plt.hist(sentiment_scores, bins=20, color='lightgreen', edgecolor='black', alpha=0.7)
        plt.title('Distribution of Sentiment Scores')
        plt.xlabel('Sentiment Score')
        plt.ylabel('Frequency')
        plt.show()

    def setupUi(self, wikipedi):
        wikipedi.setObjectName("wikipedi")
        wikipedi.resize(1200, 800)
        wikipedi.setStyleSheet("QMainWindow:{background-color:\"#E3FEF7\"}")
        self.centralwidget = QtWidgets.QWidget(wikipedi)
        self.centralwidget.setStyleSheet("background-color:\"#E3FEF7\"")
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 170, 150, 50))
        font = QtGui.QFont()
        # font.setFamily("Times New Roman")
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setStyleSheet("font: 700 30pt ;\n" "color: rgb(0, 60, 67);")
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.summary())
        self.pushButton.setGeometry(QtCore.QRect(950, 170, 160, 50))
        font = QtGui.QFont()
        # font.setFamily("Times New Roman")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("font: 700 15pt ;\n" "color: rgb(0, 60, 67);")
        self.pushButton.setObjectName("pushButton")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(325, 370, 785, 300))
        self.textBrowser.setObjectName("textBrowser")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(325, 170, 550, 50))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n" "border-color: rgb(0, 60, 67);")
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(325, 50, 550, 61))
        font = QtGui.QFont()
        # font.setFamily("Times New Roman")
        font.setPointSize(30)
        font.setItalic(False)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("font: 800 30pt ;\n" "color: rgb(0, 60, 67);")
        self.label_3.setObjectName("label_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(80, 360, 250, 61))
        font = QtGui.QFont()
        # font.setFamily("Times New Roman")
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(False)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("font: 700 30pt ;\n" "color: rgb(0, 60, 67);")
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        wikipedi.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(wikipedi)
        self.statusbar.setObjectName("statusbar")
        wikipedi.setStatusBar(self.statusbar)

        self.retranslateUi(wikipedi)
        QtCore.QMetaObject.connectSlotsByName(wikipedi)

    def retranslateUi(self, wikipedi):
        _translate = QtCore.QCoreApplication.translate
        wikipedi.setWindowTitle(_translate("wikipedi", "TextSummarization"))
        self.label.setText(_translate("wikipedi", "URL : "))
        self.pushButton.setText(_translate("wikipedi", "Summarize"))
        self.label_3.setText(_translate("wikipedi", "Summary of Text in URL"))
        self.label_2.setText(_translate("wikipedi", "Summary:"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = wikipedia_page()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
