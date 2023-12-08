import pandas as pd
import streamlit as st
from aspectBasedSentimentAnalysis import AspectSentimentAnalyzer
from constants import ASPECTS, FILENAME


raw_data = pd.read_csv(FILENAME)
analyzer = AspectSentimentAnalyzer()

def get_rank_list(options): # the options are sensitive to order
    # call model to get the ranks
    # input: ordered aspects
    # output: ranked object ids
    objects = analyzer.get_ranking_by_aspect(options)
    return objects

def display_ranked_list(objects):
    # inputs: object ids
    # outputs: dataframe for display
    display_cols = ["Clothing ID","Rating","Positive Feedback Count", "Division Name","Department Name","Class Name"]
    show_data = raw_data[raw_data['Clothing ID'].isin(objects)][display_cols].groupby("Clothing ID", as_index=False).agg({"Rating": "mean", "Positive Feedback Count": "mean", "Division Name": "unique", "Department Name": 'unique', 'Class Name':'unique'})
    return show_data.set_index("Clothing ID")

class SemanticCompare:
    def build_title(self):
        return st.title("Guess What You Like")
    def build_input(self, options):
        sentences = get_rank_list(options)
        display = display_ranked_list(sentences)
        return st.dataframe(display)

class SemanticComparePage:
    def build(self):
        compare = SemanticCompare()
        compare.build_title()
        options = st.multiselect(
            "Select the aspects you care the most:",
            ASPECTS,
            ['color', 'confortable']
        )
        compare.build_input(options=options)

page = SemanticComparePage()
page.build()
