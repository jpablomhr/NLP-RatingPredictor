import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

## Se crea el df desde reseña.csv
df_reviews = pd.read_csv('reseña.csv')

# Cambiamos el nombre de algunas columnas.
df_reviews = df_reviews.rename(columns={'Reseña': 'Review'})
df_reviews = df_reviews.rename(columns={'Estrellas': 'Rating'})

# Instalamos lo necesario de nltk para el análisis de sentimientos.
nltk.download('punkt') #Tokenize
nltk.download('stopwords') # Palabras vacías
nltk.download('punkt_tab')
nltk.download('vader_lexicon') # Puntuaciones

# Pre-procesamiento del análisis.
def preprocess_res(text):
   text = text.lower()
   words = word_tokenize(text)
   stop_words = set(stopwords.words('spanish'))
   words = [word for word in words if word.isalpha() and word not in stop_words and word not in string.punctuation]
   return " ".join(words)

sia = SentimentIntensityAnalyzer()

def getsentiment(text):
    sentiment_score = sia.polarity_scores(text)
    return sentiment_score['compound']

df_reviews['Review'] = df_reviews['Review'].fillna('Sin reseña').astype(str)

df_reviews['Cleanned Review'] = df_reviews['Review'].apply(preprocess_res)
df_reviews['Sentiment'] = df_reviews['Cleanned Review'].apply(getsentiment)

print(df_reviews.head(34))

df_reviews.to_csv('review_with_feeling.csv', index=False)



