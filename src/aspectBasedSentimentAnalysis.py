import pandas as pd
import nltk
from nltk import sent_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from preprocessing import preprocessText
from constants import FILENAME, ASPECTS

# Global variables
# FILENAME = "Womens Clothing E-Commerce Reviews.csv"
# ASPECTS = ["dress", "love", "fit", "size", "top", "color", "look", "wear", "fabric", "cute", "flattering", "comfortable"]

nltk.download('vader_lexicon') 
nltk.download('punkt')

class AspectSentimentAnalyzer:
    def __init__(self):
        # Load and preprocess the data
        self.df = pd.read_csv(FILENAME)
        self.df.drop(columns=self.df.columns[0], axis=1, inplace=True)
        self.df['Combined_Text'] = self.df['Review Text'].fillna('') + ' ' + self.df['Title'].fillna('')
        self.df['Weight'] = self.df['Positive Feedback Count'].fillna(0) + 1
        self.sia = SentimentIntensityAnalyzer()
        self._prepare_sentiments()

    def _find_aspect_sentences(self, text, aspect):
        return [sentence for sentence in sent_tokenize(text) if aspect in sentence]

    def _analyze_aspect_sentiment(self, aspect_sentences):
        if not aspect_sentences:
            return 0
        scores = [self.sia.polarity_scores(sentence)['compound'] for sentence in aspect_sentences]
        return sum(scores) / len(scores)

    def _prepare_sentiments(self):
        for aspect in ASPECTS:
            self.df[aspect + '_sentences'] = self.df['Combined_Text'].apply(lambda text: self._find_aspect_sentences(text, aspect))
            self.df[aspect + '_sentiment'] = self.df[aspect + '_sentences'].apply(self._analyze_aspect_sentiment)
            self.df[aspect + '_weighted_sentiment'] = self.df[aspect + '_sentiment'] * self.df['Weight']

        self._aggregate_sentiments()

    def _aggregate_sentiments(self):
        agg_columns = {aspect + '_weighted_sentiment': 'sum' for aspect in ASPECTS}
        agg_columns['Weight'] = 'sum'
        self.df_grouped = self.df.groupby('Clothing ID').agg(agg_columns).reset_index()

        for aspect in ASPECTS:
            weighted_col = aspect + '_weighted_sentiment'
            self.df_grouped[aspect + '_sentiment'] = self.df_grouped[weighted_col] / self.df_grouped['Weight']
            self.df_grouped.drop(columns=[weighted_col], inplace=True)

    def get_ranking_by_aspect(self, input_aspects, N=10):
        def calculate_combined_score(row, aspect_cols):
            non_zero_scores = [score for score in row[aspect_cols] if score != 0]
            return sum(non_zero_scores) / len(non_zero_scores) if non_zero_scores else 0

        aspect_cols = [aspect + '_sentiment' for aspect in input_aspects]
        df_selected = self.df_grouped[['Clothing ID'] + aspect_cols]
        df_selected['combined_score'] = df_selected.apply(calculate_combined_score, axis=1, args=(aspect_cols,))
        df_ranked = df_selected.sort_values(by='combined_score', ascending=False)
        return df_ranked[['Clothing ID', 'combined_score']].head(N)

# Usage
# analyzer = AspectSentimentAnalyzer()
# print(analyzer.get_ranking_by_aspect(["color", "fit", "fabric"]))