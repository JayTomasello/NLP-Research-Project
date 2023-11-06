"""
mainSA2.py

This program is designed to be used as a launchpad for accessing the sentiment analysis
capabilities (i.e., functions) of the files pushshiftDFSetupSA.py, nrcLexSA.py, and vaderSA.py.

Author: Joseph A. Tomasello
"""


"""
BEGIN - SCRIPT PREPARATION
"""
from pushshiftDFSetupSA import *
from vaderSA import *
from nrcLexSA2 import *
"""
END - SCRIPT PREPARATION 
"""


"""
BEGIN - FUNCTIONS
"""
# This function generates all the NRC Lexicon and VADER plots available through nrcLexSA.py and vaderSA.py
def generate_all_nrc_charts(dataframe, dataset_name, charting_interval, dataset_start_date, dataset_end_date, datetime_column):

    # NRC Plots
    bar_dict = nrc_chart_emotions_full_barh(dataframe, 'NRC Lexicon - ' + dataset_name + '\nEmotion Score Totals')
    '''nrc_chart_pos_neg_full_bar(dataframe, 'NRC Lexicon - ' + dataset_name + '\nSentiment Score Totals')
    nrc_chart_emotions_full_pie(dataframe, 'NRC Lexicon - ' + dataset_name + '\nEmotion Score Percentages')
    nrc_chart_pos_neg_full_pie(dataframe, 'NRC Lexicon - ' + dataset_name + '\nSentiment Score Percentages')'''
    full_nrc_dict = nrc_interval_catalogue(dataframe, charting_interval, dataset_start_date, dataset_end_date, datetime_column)
    nrc_chart_emotions_interval_line(full_nrc_dict, 'NRC Lexicon - ' + dataset_name + '\nEmotion Scores Over Time')
    #nrc_chart_pos_and_neg_interval_line(full_nrc_dict, 'NRC Lexicon - ' + dataset_name + '\nSentiment Scores Over Time')

    return bar_dict

def generate_all_vader_charts(dataframe, dataset_name, charting_interval, dataset_start_date, dataset_end_date, datetime_column):

    # VADER Plots
    bar_dict = vader_chart_full_bar(dataframe, 'VADER - ' + dataset_name + '\nSentiment Post Counts')
    vader_chart_full_pie(dataframe, 'VADER - ' + dataset_name + '\nSentiment Post Counts')
    full_vader_dict = vader_interval_catalogue(dataframe, charting_interval, dataset_start_date, dataset_end_date, datetime_column)
    vader_chart_interval_line(full_vader_dict, 'VADER - ' + dataset_name + '\nSentiment Post Counts')

    return bar_dict

"""
END - FUNCTIONS
"""


"""
BEGIN - MAIN
"""
def main():

    # UNUSED FUNCTIONS THAT ARE ALSO AVAILABLE
    '''
    # Creates a dataframe usable for a sentiment analysis
    initial_dataframe = create_dataframe('dataset_all_posts_4years_sorted', 'selftext')
    
    # Performs an analysis with NRC Lexicon and adds the results to the dataframe
    dataframe_with_nrc = nrc_lexicon_analysis(initial_dataframe)
    
    # Performs an analysis with VADER and adds the results to the dataframe
    dataframe_with_nrc_and_vader = vader_analysis(dataframe_with_nrc)
    
    # Saves the specified dataframe as a csv file
    save_dataframe_as_csv(dataframe_with_nrc_and_vader, 'dataset_all_posts_4years_SA.csv')
    '''

    # Used to store the details of the dataset being used
    dataset_name = 'dataset_all_posts_4years_SA.csv'
    dataset_start_date = '2018-03-11'
    dataset_end_date = '2022-03-11'
    date_column_name_in_dataset = 'datetime'
    monthly_charting_interval = 2 # Used to chart the dataset over time (in this case, 2 months at a time)

    # Used to assemble the dataframe from a csv file
    full_dataset_dataframe = pd.read_csv(dataset_name, encoding="utf8")

    # Full dataset charting (r/mentalhealth + r/depression + r/Anxiety)
    full_bar_dict = generate_all_vader_charts(full_dataset_dataframe, 'Full Dataset', monthly_charting_interval, dataset_start_date, dataset_end_date, date_column_name_in_dataset)
    full_bar_dict2 = generate_all_nrc_charts(full_dataset_dataframe, 'Full Dataset', monthly_charting_interval, dataset_start_date, dataset_end_date, date_column_name_in_dataset)

    # Charting only r/mentalhealth data
    only_mental_health_dataframe = subreddit_filter(full_dataset_dataframe, 'subreddit', 'r/depression')
    only_mental_health_dataframe = subreddit_filter(only_mental_health_dataframe, 'subreddit', 'r/Anxiety')
    mental_health_bar_dict = generate_all_vader_charts(only_mental_health_dataframe, 'r/mentalhealth', monthly_charting_interval, dataset_start_date, dataset_end_date, date_column_name_in_dataset)
    mental_health_bar_dict2 = generate_all_nrc_charts(only_mental_health_dataframe, 'r/mentalhealth', monthly_charting_interval, dataset_start_date, dataset_end_date, date_column_name_in_dataset)

    # Charting only r/depression data
    only_depression_dataframe = subreddit_filter(full_dataset_dataframe, 'subreddit', 'r/mentalhealth')
    only_depression_dataframe = subreddit_filter(only_depression_dataframe, 'subreddit', 'r/Anxiety')
    depression_bar_dict = generate_all_vader_charts(only_depression_dataframe, 'r/depression', monthly_charting_interval, dataset_start_date, dataset_end_date, date_column_name_in_dataset)
    depression_bar_dict2 = generate_all_nrc_charts(only_depression_dataframe, 'r/depression', monthly_charting_interval, dataset_start_date, dataset_end_date, date_column_name_in_dataset)

    # Charting only r/Anxiety data
    only_anxiety_dataframe = subreddit_filter(full_dataset_dataframe, 'subreddit', 'r/mentalhealth')
    only_anxiety_dataframe = subreddit_filter(only_anxiety_dataframe, 'subreddit', 'r/depression')
    anxiety_bar_dict = generate_all_vader_charts(only_anxiety_dataframe, 'r/Anxiety', monthly_charting_interval, dataset_start_date, dataset_end_date, date_column_name_in_dataset)
    anxiety_bar_dict2 = generate_all_nrc_charts(only_anxiety_dataframe, 'r/Anxiety', monthly_charting_interval, dataset_start_date, dataset_end_date, date_column_name_in_dataset)

    # Charting the full dataset alongside its 3 component subreddits
    vader_chart_multiple_bars('VADER - Sentiment Post Counts', Full_Dataset=full_bar_dict, mentalhealth=mental_health_bar_dict, depression=depression_bar_dict, Anxiety=anxiety_bar_dict)
    #nrc_chart_emotions_multiple_bars('NRC Lexicon - Emotion Score Totals', Full_Dataset=full_bar_dict2, mentalhealth=mental_health_bar_dict2, depression=depression_bar_dict2, Anxiety=anxiety_bar_dict2)

if __name__== "__main__" : main()

"""
END - MAIN
"""
