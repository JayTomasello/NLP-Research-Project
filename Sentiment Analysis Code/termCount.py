"""
termCount.py

This program is designed to count and plot the most used significant terms within the 
target text of the dataframe passed to it.

Author: Joseph A. Tomasello
"""

"""
BEGIN - SCRIPT PREPARATION
"""
import matplotlib.pyplot as mp
from pushshiftDFSetupSA import *
import ast
import csv
"""
END - SCRIPT PREPARATION
"""

"""
BEGIN - FUNCTIONS
"""
# Function that creates a dict of body_text terms and their respective counts 
# in the dataframe passed to it
def count_terms(dataframe):
    unique_word_dict = {}

    for column in dataframe['body_text_lemmatized']:
        column = ast.literal_eval(column)
        for j in column:
            if j in unique_word_dict:
                unique_word_dict[j] += 1
            else:
                unique_word_dict[j] = 1
    
    return unique_word_dict

# Function that saves a dict of term counts to a csv file
def save_term_counts_to_csv(unique_word_dict, file_name):
    # Sorts the dict so that the terms are written to the csv file in descending order
    sorted_dict = dict(sorted(unique_word_dict.items(), key=lambda item: item[1]))
    
    # Writes the terms to a csv file (entry format: term,count)
    term_w = csv.writer(open(file_name, "w", encoding="utf-8"))
    for key, val in sorted_dict.items():
        term_w.writerow([key, val])

# Function that generates a dict of terms using the txt file passed to it
def generate_term_dict_from_txt(term_txt_file):
    term_dict = {}
    f_data = open(term_txt_file, "r")
    lines = [line for line in f_data.readlines() if line.strip()]
    for line in lines:
        dict_entry = line.split(",")
        print(term_dict)
        term_dict[dict_entry[0]] = dict_entry[1].strip()
    return term_dict

# Function that generates a horizontal bar plot to visualize the most used 
# terms in the dataset being evaluated
def chart_top_terms_full_barh(dict, plot_title):

    #sorted_dict = dict(sorted(dict.items(), key=lambda item: item[1]))

    term_names_list = []
    term_counts_list = []

    # Populates the two dictionaries used to generate the plot
    for key, value in dict.items():
        term_names_list.append(key)
        term_counts_list.append(int(value))

    # Accesses the 25 bottom (highest) term entries
    term_names_list = term_names_list[-25:]
    term_counts_list = term_counts_list[-25:]

    # Generates the bar plot
    ax = mp.barh(term_names_list, term_counts_list)

    # fmt='%d' disables scientific notation for the exact value bar labels
    mp.bar_label(ax, fmt='%d')

    # Introduces comma separators to the number values displayed across the x-axis
    current_values = mp.gca().get_xticks()
    mp.gca().set_xticklabels(['{:,.0f}'.format(x) for x in current_values])

    # Labels and displays the bar plot
    mp.title(plot_title)
    mp.xlabel('Term Count')
    mp.ylabel('Terms')
    mp.show()
"""
END - FUNCTIONS
"""