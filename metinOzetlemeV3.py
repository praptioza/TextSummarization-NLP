import bs4 as bs
import urllib.request
import re
import nltk
import heapq

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Wikipedia URL of the topic you want to summarize
data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Natural_language_processing')
read_text = data.read()

parsed_text = bs.BeautifulSoup(read_text,'lxml')

paragraphs = parsed_text.find_all('p')

text = ""

for p in paragraphs:
    text += p.text

text = re.sub(r'\[[0-9]*\]', ' ', text)
text = re.sub(r'\s+', ' ', text)

print(text)

# Seperate the sentences
sentences = nltk.sent_tokenize(text)

# Remove punctuation marks to find which word is repeated most frequently
text_with_words = re.sub('[^a-zA-Z]', ' ', text )
text_with_words = re.sub(r'\s+', ' ', text_with_words)

# Get the english stopwords
stopwords = nltk.corpus.stopwords.words('english')



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

# en cok tekrar eden agirlikli kelimeyi aliyoruz.
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


# Take the top 7 sentences with the highest score. We can take more depending on the value we provide.
summary_sentence = heapq.nlargest(7, sentence_score, key=sentence_score.get)

summary = ' '.join(summary_sentence)
print("Summary::")
print(summary)

f = open("textSummary.txt", "w")
f.write(summary)
f.close()