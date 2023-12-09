# CourseProject

Please fork this repository and paste the github link of your fork on Microsoft CMT. Detailed instructions are on Coursera under Week 1: Course Project Overview/Week 9 Activities.

# Fashion Recommendations with In-depth Review Analysis

## Datasets

Datasets we used are in folder `src`
* "Womens Clothing E-Commerce Reviews.csv" (Main Data), from [Kaggle](https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews)
* "background_data_dev.txt" (Background Data), from [github](https://github.com/NJUNLP/DMASTE/blob/main/dataset/fashion/dev.txt)

## Initial data exploration

This dataset contains several useful columns. Among them, we can use "Review Text" and "Title" as input for sentiment analysis. There are some basic stats for the data on [Kaggle](https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews). Besides that, we also plotted some histograms to better understand the data, which can be found in `src/data_stats.ipynb`.

## Preprocessing

preprocessing can be found in `src/preprocessing.ipynb` and `src/preprocessing.py`. Those two are the same functionality-wise with `src/preprocessing.py` to be used as util in other scripts. Several preprocessing steps are used here: expand contractions, lowering casing, remove punctuation, remove numbers, tokenization, remove stopwords, lemamtization. Expanding the contractions is to avoid aspect words like "im" in the later analysis. And nltk libraries are used in this process.

## aspect keywords extraction

aspect keywords extraction can be found in `src/aspectExtraction.ipynb`. There are two different approaches used here.

1. extract list of aspect keywords

    Here we were trying to extract each individual aspect words by using the nltk library. Noun and adjective or numerals are extracted here. We also took a look at the background data here.

2. aspect words cluster

    Aspect words clusters are extracted here using nltk and gensim libraries (LDA model).

After getting the aspect words from the two approaches above, we further did some manual adjustment and came up with the list of aspect words to be used in the sentiment analysis later.

## aspect based sentiment analysis

Aspect based sentiment analysis can be found in `src/aspectBasedSentimentAnalysis.ipynb` and `src/aspectBasedSentimentAnalysis.py`, with the latter to be called by the UI.

With the aspect keyword list we got from the previous step, sentiment analysis were performed for each review. Class AspectSentimentAnalyzer wrapped several steps, including reading in data, preprocessing, analyzing aspect sentiment for each review, aggregating sentiment by considering the "Positive Feedback Count", providing a function to be called by the UI to return the ranked list of clothing ids with the input aspects. We joined the "Review Text" and "Title" here to account for the impact from both of them. 

Sample usage of Class AspectSentimentAnalyzer:

`analyzer = AspectSentimentAnalyzer()`

`print(analyzer.get_ranking_by_aspect(["color", "fit", "fabric"]))`

## Feedbacks

Feedbacks can be found in `src/aspectBasedSentimentAnalysis.ipynb` at the very end. We did some manual testing to check the performance of the model. 


## To start the UI
```
python3.11 -m venv venv
source venv/bin/activate
python3.11 -m pip install -r requirements.txt

python3.11 -m streamlit run ./src/review_ui.py
```
