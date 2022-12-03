import pandas as pd
from textblob import TextBlob
from sklearn.model_selection import train_test_split

from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
import string

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.linear_model import LogisticRegression

def getting_score(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    return polarity

def spacy_tokenizer(utterance):
    tokens = parser(utterance)
    return [token.lemma_.lower().strip() for token in tokens if token.text.lower().strip() not in stopwords and token.text not in punctuations]


df = pd.read_csv('stockerbot-export.csv', delimiter=',', encoding='latin-1', names=['id','text','timestamp','source','syboml','company names','url','verified'])


for i in df.columns:
    if i!="text":
        del df[i]

score_list = []

for i in df['text']:
    if getting_score(i) > 0:
        score_list.append(1)
    elif getting_score(i) == 0:
        score_list.append(0)
    elif getting_score(i) < 0:
        score_list.append(-1)

column_name = ['sentiment']
scores_df = pd.DataFrame(score_list,columns=column_name)
df = df.join(scores_df,rsuffix='_right')

df = df.iloc[1:]


reviews = df['text'].values
labels = df['sentiment'].values
reviews_train, reviews_test, y_train, y_test = train_test_split(reviews,labels,train_size=0.7,test_size=0.3,
                                                                random_state=0,stratify=True)

punctuations = string.punctuation
parser = English()
stopwords = list(STOP_WORDS)

vectorizerr = CountVectorizer(tokenizer=spacy_tokenizer, ngram_range=(1, 1))
vectorizerr.fit(reviews_train)

x_train = vectorizerr.transform(reviews_train)
x_test = vectorizerr.transform(reviews_test)

classifier = LogisticRegression()
classifier.fit(x_train,y_train)

accuracy = classifier.score(x_test,y_test)
print("Accuracy:",accuracy)



