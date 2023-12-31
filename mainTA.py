"""
mainTA.py

This program is designed to be used as a launchpad for accessing the topic modeling
capabilities (i.e., functions) of the files pushshiftDFSetupTA.py and topicAnalysisV3.py.

Author: Joseph A. Tomasello
"""


"""
BEGIN - SCRIPT PREPARATION
"""
from pushshiftDFSetupTA import *
from topicAnalysisV3 import *
"""
END - SCRIPT PREPARATION 
"""


"""
BEGIN - FUNCTIONS
"""

"""
END - FUNCTIONS
"""


"""
BEGIN - MAIN
"""
def main():

    term_dict_all = generate_term_dict_from_txt("term_counts_all.txt")
    term_dict_Anxiety = generate_term_dict_from_txt("term_counts_Anxiety.txt")
    term_dict_depression = generate_term_dict_from_txt("term_counts_depression.txt")
    term_dict_mentalhealth = generate_term_dict_from_txt("term_counts_mental_health.txt")
    
    chart_top_terms_full_barh(term_dict_all, "Total Term Counts - Full Dataset")
    chart_top_terms_full_barh(term_dict_Anxiety, "Total Term Counts - r/Anxiety")
    chart_top_terms_full_barh(term_dict_mentalhealth, "Total Term Counts - r/mentalhealth")
    chart_top_terms_full_barh(term_dict_depression, "Total Term Counts - r/depression")

if __name__== "__main__" : main()

"""
END - MAIN
"""
