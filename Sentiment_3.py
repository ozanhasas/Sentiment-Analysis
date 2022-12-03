import pandas as pd

from sklearn.model_selection import train_test_split

from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
import string

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.linear_model import LogisticRegression

df = pd.read_csv('all-data.csv',  delimiter=',', encoding='latin-1', names=['Sentiment', 'Text'])
sentiment  = {'negative': 0,'neutral': 1,'positive':2}

df.Sentiment = [sentiment[item] for item in df.Sentiment]
df2 = pd.read_csv('stock_data.csv',  sep='delimiter',delimiter=',', encoding='latin-1', names=['Text', 'Sentiment'])

df2 = df2[df2 ['Sentiment'] != 'Sentiment']
sentiment  = {'-1': 0, '1': 2}

df2.Sentiment = [sentiment[item] for item in df2.Sentiment]
df = df.append(df2, ignore_index=True)


reviews = df['Text'].values
labels = df['Sentiment'].values

reviews_train, reviews_test, y_train, y_test = train_test_split(reviews,labels,test_size=0.2,random_state=21000)

punctuations = string.punctuation
parser = English()
stopwords = list(STOP_WORDS)

def spacy_tokenizer(utterance):
    tokens = parser(utterance)
    return [token.lemma_.lower().strip() for token in tokens if token.text.lower().strip() not in stopwords and token.text not in punctuations]


vectorizer = CountVectorizer(tokenizer=spacy_tokenizer,ngram_range=(1,1))
vectorizer.fit(reviews_train)

x_train = vectorizer.transform(reviews_train)
x_test = vectorizer.transform(reviews_test)

classifier = LogisticRegression()
classifier.fit(x_train,y_train)

accuracy = classifier.score(x_test,y_test)
print("Accuracy:",accuracy)


new_reviews = ['Old version of python useless', 'Very good effort, but not five stars', 'Clear and concise']
X_new = vectorizer.transform(new_reviews)
classifier.predict(X_new)
print(classifier.predict(X_new))


