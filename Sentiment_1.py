from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

tmp_url = 'https://finviz.com/quote.ashx?t='

ticker = ''
tickers = []

while ticker != '0':
    ticker = input("Enter a ticker or enter 0 to see results")
    if ticker != '0':
        tickers.append(ticker)

tickers_news = {}
headers = {'user-agent': 'my-app/0.0.1'}

for ticker_name in tickers:
    url = tmp_url + ticker_name
    r = Request(url, headers=headers)
    response = urlopen(r)
    soup = BeautifulSoup(response, "html.parser")
    news_table = soup.find(id='news-table')
    tickers_news[ticker_name] = news_table

parsed_news = []
for name_ticker, news_list in tickers_news.items():
    for each_news in news_list.findAll('tr'):
        news_content = each_news.a.get_text()
        ticker_name = name_ticker
        parsed_news.append([ticker_name, news_content])


def getting_score(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    return polarity


column_names = ['ticker_name', 'content']
scored_news = pd.DataFrame(parsed_news, columns=column_names)
scores_list = scored_news['content'].apply(getting_score).tolist()
column_name = ['scores']
scores_df = pd.DataFrame(scores_list,columns=column_name)
scored_news = scored_news.join(scores_df, rsuffix='_right')

scored_news.to_excel(r'C:\Users\arif_\OneDrive\Masaüstü\Tickers.xlsx',index=False,header=True)

percentage_dic = {}


for x in range(len(tickers)):
    dic_of_percentage = {'positive': 0, 'negative': 0, 'neutral': 0}
    for a in scored_news['scores'][x*100:(x*100)+100]:
        if a == 0:
            dic_of_percentage['neutral'] += 1
        elif a < 0:
            dic_of_percentage['negative'] += 1
        elif a > 0:
            dic_of_percentage['positive'] += 1
    percentage_dic[tickers[x]] = dic_of_percentage


def do_graph(dic,nameof_ticker):
    labels = ['Positive ['+str(dic['positive'])+'%]','Neutral ['+str(dic['neutral'])+'%]','Negative ['+str(dic['negative'])+'%]']
    sizes = [dic['positive'], dic['neutral'], dic['negative']]
    colors = ['yellowgreen','gray','red']
    fig, ax = plt.subplots()
    ax.pie(sizes,labels=labels,startangle=90,colors=colors)
    plt.title("Analysis of news about "+nameof_ticker)
    ax.axis('equal')


for i in tickers:
    do_graph(percentage_dic[i], i)

plt.show()











