"""
pushshift.py

This program accesses the Pushshift API to search and collect post and
comment data from Reddit.com through the specification of a collection 
timeline, subreddit, and search term.

The collected post and comment datasets are stored to csv files.

Authors: Joseph A. Tomasello and Silvertongue26
Unaltered Base Code: https://github.com/Silvertongue26/reddit_api/blob/main/reddit6.py
"""


"""
BEGIN - Script preparation
Section for importing libraries and setting up basic environment configurations
"""
from psaw import PushshiftAPI                               #Importing wrapper library for reddit(Pushshift)
import datetime as dt                                       #Importing library for date management
import pandas as pd                                         #Importing library for data manipulation in python
import matplotlib.pyplot as plt                             #Importing library for creating interactive visualizations in Python
from pprint import pprint                                   #Importing for displaying lists in the "pretty" way (Not required)

pd.set_option("display.max_columns", None)                  #Configuration for pandas to show all columns on dataframe
api = PushshiftAPI()                                        #We create an object of the API
"""
END - Script preparation 
"""



"""
BEGIN - DATAFRAME GENERATION FUNCTIONS

Here we are going to make a request to through the API
to the selected subreddit and the results are going 
to be placed inside a pandas dataframe
"""

"""FOR POSTS"""
def data_prep_posts(subreddit, start_time, end_time, filters, limit):
    if(len(filters) == 0):
        filters = ['id', 'author', 'created_utc',
                   'domain', 'url',
                   'title', 'num_comments', 'selftext', 'link_flair_richtext']
                   #We set by default some columns that will be useful for data analysis

    posts = list(api.search_submissions(
        subreddit=subreddit,                                #We set the subreddit we want to audit
        after=start_time,                                   #Start date
        before=end_time,                                    #End date
        filter=filters,                                     #Column names we want to get from reddit
        limit=limit))                                       #Max number of posts we wanto to recieve

    return pd.DataFrame(posts)                              #Return dataframe for analysis


"""FOR COMMENTS"""
def data_prep_comments(term, start_time, end_time, filters, limit):
    if (len(filters) == 0):
        filters = ['id', 'author', 'created_utc',
                   'body', 'permalink', 'subreddit']        #We set by default some columns that will be useful for data analysis

    comments = list(api.search_comments(
        q=term,                                             #We set the subreddit we want to audit
        after=start_time,                                   #Start date
        before=end_time,                                    #End date
        filter=filters,                                     #Column names we want to get from reddit
        limit=limit))                                       #Max number of comments we wanto to recieve
    return pd.DataFrame(comments)                           #Return dataframe for analysis

"""
END - DATAFRAME GENERATION FUNCTIONS
"""



"""
BEGIN - FUNCTIONS
"""
###Function to plot the number of posts per day on the specified subreddit
def count_posts_per_date(df_p, title, xlabel, ylabel):
    df_p.groupby([df_p.datetime.dt.date]).count().plot(y='id', rot=45, kind='bar', label='Posts')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

###Function to plot the mean of comments per day on the specified subreddit
def mean_comments_per_date(df_p, title, xlabel, ylabel):
    df_p.groupby([df_p.datetime.dt.date]).mean().plot(y='num_comments', rot=45, kind='line', label='Comments')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

###Function to plot the most active users on the subreddit
def most_active_author(df_p, title, xlabel, ylabel, limit):
    df_p.groupby([df_p.author]).count()['id'].nlargest(limit).sort_values(ascending=True).plot(y='id', rot=45, kind='barh', label='Users')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

###Function to que the orgin form the crossposting
def get_posts_orign(df_p, title, xlabel, ylabel, limit, subreddit):
    domains = df_p[(df_p.domain != 'reddit.com') & (df_p.domain != f'self.{subreddit}') & (df_p.domain != 'i.redd.it')]
    domains.groupby(by='domain').count()['id'].nlargest(limit).sort_values(ascending=True).plot(kind='barh', rot=45, x='domain', label='# of posts', legend=True, figsize=(8,13))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

###Gets most active subrredits according to search term
def get_subreddits(df_p, title, xlabel, ylabel, limit):
    df_p.groupby(by='subreddit').count()['id'].nlargest(limit).sort_values(ascending=True).plot(kind='barh', x='subreddit', label='Subreddit', legend=True, figsize=(8,13))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


"""
END - FUNCTIONS
"""


def main():
    subreddit = "mentalillness"                               #Name of the subreddit we are auditing
    start_time = int(dt.datetime(2018, 3, 11).timestamp()) #We define the starting date for our search (Format: Year, Month, Day)
    end_time = int(dt.datetime(2022, 3, 11).timestamp())   #We define the ending date for our search (Format: Year, Month, Day)
    filters = []                                           #We don´t want specific filters
    limit = 10000000                                       #Number of elelemts we want to recieve

    """Here we are going to get subreddits for a brief analysis"""
    df_p = data_prep_posts(subreddit,start_time,
                         end_time,filters,limit)           #Call function for dataframe creation of comments

    print(len(df_p))

    df_p['datetime'] = df_p['created_utc'].map(
        lambda t: dt.datetime.fromtimestamp(t))
    df_p = df_p.drop('created_utc', axis=1)                #Drop the column on timestamp format
    df_p = df_p.sort_values(by='datetime')                 #Sort the Row by datetime
    df_p["datetime"] = pd.to_datetime(df_p["datetime"])    #Convert timestamp format to datetime for data analysis


    df_p.to_csv(f'dataset_{subreddit}_posts_4years.csv', sep=',', # Save the post dataset on a csv file for future analysis
                header=True, index=False, columns=[
            'id', 'author', 'datetime', 'domain',
            'url', 'title', 'num_comments', 'selftext', 'link_flair_richtext'
        ])

    count_posts_per_date(df_p, 'Post per day', 'Days',     #Function to plot the number of posts per day on the specified subreddit
                         'posts')
    mean_comments_per_date(df_p,                           #Function to plot the mean of comments per day on the specified subreddit
                           'Average comments per day',
                           'Days', 'comments')
    most_active_author(df_p, 'Most active users',          #Function to plot the most active users on the subreddit
                       'Posts', 'Users', 10)
    get_posts_orign(df_p, 'Origin of crosspostings',       #Function to que the orgin form the crossposting
                    'Crossposts', 'Origins', 10,
                    subreddit)
'''
    """Here we are going to get comments for a brief analysis"""
    term = 'depression'                                     #Term we want to search for
    limit = 10                                              #Number of elelemts we want to recieve
    df_c = data_prep_comments(term, start_time,             #Call function for dataframe creation of comments
                         end_time, filters, limit)

    df_c['datetime'] = df_c['created_utc'].map(
        lambda t: dt.datetime.fromtimestamp(t))
    df_c = df_c.drop('created_utc', axis=1)                #Drop the column on timestamp format
    df_c = df_c.sort_values(by='datetime')                 #Sort the Row by datetime
    df_c["datetime"] = pd.to_datetime(df_c["datetime"])    #Convert timestamp format to datetime for data analysis
'''

#    df_c.to_csv(f'dataset_{term}_comments.csv', sep=',',   # Save the comment dataset on a csv file for future analysis
#                header=True, index=False, columns=[
#            'id', 'author', 'datetime',
#                   'body', 'permalink', 'subreddit'
#        ])                     

#    get_subreddits(df_c, 'Most active subreddit', 'Posts',  #Gets most active subrredits according to search term
#                   'Subreddits', 10)




if __name__== "__main__" : main()
