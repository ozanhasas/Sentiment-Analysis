import pandas as pd

df = pd.read_csv('stockerbot-export.csv', delimiter=',', encoding='latin-1', names=['text'])
print(df.head())