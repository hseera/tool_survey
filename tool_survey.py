# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

import warnings
warnings.filterwarnings("ignore")
 
FILE_TO_WRITE = "./sample_files/full_list.csv"
 
def split_string_in_column(file_name):
    
    try:
        tools_df = pd.read_csv(file_name)
        
        
        #Get tools used in last three year data
        tools_used = tools_df['tools_used'].str.split(", ", expand = True) #split each row in the column with ", "
        tools_used=pd.melt(tools_used, value_name='all') #combine all columns into one column
        
        tools_used['all'] = tools_used['all'].str.capitalize()
        tools_used['all'] = tools_used['all'].str.replace(r'(^.*house.*$)', 'inhouse')
        tools_used['all'] = tools_used['all'].str.replace(r'(^.*internal.*$)', 'inhouse')
        tools_used_table = pd.pivot_table(tools_used, values='all',columns=['all'], aggfunc='count')
        
        
        #Get current tool data
        current_tool = tools_df['current_tool'].str.split(", ", expand = True) #split each row in the column with ", "
        current_tool=pd.melt(current_tool) #combine all columns into one column
        current_tool['value'] = current_tool['value'].str.capitalize()
        current_tool['value'] = current_tool['value'].str.replace(r'(^.*house.*$)', 'Inhouse/Custom')
        current_tool['value'] = current_tool['value'].str.replace(r'(^.*Internal.*$)', 'Inhouse/Custom')
        current_tool['value'] = current_tool['value'].str.replace(r'(^.*Python.*$)', 'Inhouse/Custom')
        current_tool_table = pd.pivot_table(current_tool, values='value',columns=['value'], aggfunc='count')
        
        
        #Get favourite tool data
        fav_tool = tools_df['fav_tool'].str.split(", ", expand = True) #split each row in the column with ", "
        fav_tool=pd.melt(fav_tool) #combine all columns into one column
        
        fav_tool['value'] = fav_tool['value'].str.capitalize()
        fav_tool_table = pd.pivot_table(fav_tool, values='value',columns=['value'], aggfunc='count')
        
        #Get country data
        country = Counter(tools_df['country'])
        country_list = pd.DataFrame(country.items())
        country_list.columns = ['country','count']
        
        
        #Get current industry data
        current_industry = Counter(tools_df['current_industry'])
        current_industry_list = pd.DataFrame(current_industry.items())
        current_industry_list.columns = ['industry','count']
        
        
        
#        #Get Total Performance Testing Experience
#        experience = tools_df['experience'].str.split(", ", expand = True) #split each row in the column with ", "
#        experience=pd.melt(experience) #combine all columns into one column
#        
#        experience['value'] = experience['value'].str.capitalize()
#        experience_table = pd.pivot_table(experience, values='value',columns=['value'], aggfunc='count')
#        
        #Get virtual users load tested to in current engagement
        # virtual_users = tools_df['virtual_users'].str.split(", ", expand = True) #split each row in the column with ", "
        # virtual_users=pd.melt(virtual_users) #combine all columns into one column
        # virtual_users.sort_values(["value"], ascending=True)
        
        # virtual_users_table = pd.pivot_table(virtual_users, values='value',columns=['value'], aggfunc='count')
        
        # print(virtual_users_table)
        # #virtual_users_table = virtual_users_table.T.sort_values(by ='value')
        
        tools_used_chart(tools_used_table.T)
        current_tool_chart(current_tool_table.T)
        fav_tool_chart(fav_tool_table.T) 
        country_chart(country_list)
        current_industry_chart(current_industry_list)
        title_word_chart(tools_df['title'])
        
    except Exception as e:
        print(e)

def autopct(pct):
    return ('%1.f%%' % pct) if pct > 1 else ''

def title_word_chart(title_list):
    text = (title_list.str.rstrip()).values
    wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='salmon', colormap='Pastel1', 
                          collocations=False, stopwords = STOPWORDS).generate(" ".join(text)) # adds apostrophe if you use str(text) 
    
    plt.figure(figsize=(40, 30))
    plt.imshow(wordcloud) 


def current_industry_chart(current_industry):
    current_industry = current_industry.sort_values(by = 'count', ascending=False)
    bar,ax = plt.subplots(figsize=(10,10))
    ax = sns.barplot(x='count', y='industry', data=current_industry ,orient='h')
    ax.set_xlabel ("Count")
    ax.set_ylabel ("Industry")
    for rect in ax.patches:
        ax.text (rect.get_width(), rect.get_y() + rect.get_height() / 2,"%d"% rect.get_width(), weight='bold' )


def country_chart(country):
    country = country.sort_values(by = 'count', ascending=False)
    bar,ax = plt.subplots(figsize=(10,10))
    ax = sns.barplot(x='count', y='country', data=country ,orient='h')
    ax.set_xlabel ("Count")
    ax.set_ylabel ("Country")
    for rect in ax.patches:
        ax.text (rect.get_width(), rect.get_y() + rect.get_height() / 2,"%d"% rect.get_width(), weight='bold' )
    

def tools_used_chart(tools_used):
    tools_used = tools_used.sort_values(by = 'variable', ascending=False)
    bar,ax = plt.subplots(figsize=(10,10))
    ax = sns.barplot(x="variable", y=tools_used.index, data=tools_used, ci=None, palette="muted",orient='h' )
    #ax.set_title("In past three years, for your work, which load test tools have you used the most?", fontsize=13)
    ax.set_xlabel ("Count")
    ax.set_ylabel ("Tools Used")
    for rect in ax.patches:
        ax.text (rect.get_width(), rect.get_y() + rect.get_height() / 2,"%d"% rect.get_width(), weight='bold' )

def current_tool_chart(current_tool):
    current_tool = current_tool.sort_values(by = 'variable', ascending=False)
    bar,ax = plt.subplots(figsize=(10,10))
    ax = sns.barplot(x="variable", y=current_tool.index, data=current_tool, ci=None, palette="muted",orient='h' )
    #ax.set_title("Which load test tool are you using in your current engagement/job?", fontsize=13)
    ax.set_xlabel ("Count")
    ax.set_ylabel ("Current Tool")
    for rect in ax.patches:
        ax.text (rect.get_width(), rect.get_y() + rect.get_height() / 2,"%d"% rect.get_width(), weight='bold' )


def fav_tool_chart(fav_tool):
    fav_tool = fav_tool.sort_values(by = 'variable', ascending=False)
    bar,ax = plt.subplots(figsize=(10,10))
    ax = sns.barplot(x="variable", y=fav_tool.index, data=fav_tool, ci=None, palette="muted",orient='h' )
    #ax.set_title("Which is your favorite load test tool(/load test platform)?", fontsize=13)
    ax.set_xlabel ("Count")
    ax.set_ylabel ("Favorite Tool")
    for rect in ax.patches:
        ax.text (rect.get_width(), rect.get_y() + rect.get_height() / 2,"%d"% rect.get_width(), weight='bold' )

def experience_chart(experience):
    bar,ax = plt.subplots(figsize=(10,6))
    ax = sns.barplot(x=experience.index, y="variable", data=experience, ci=None, palette="muted",orient='v' )
    #ax.set_title("How long have you been doing performance testing?", fontsize=13)
    ax.set_xlabel ("Years of Experience")
    ax.set_ylabel ("Count")
    
def virtual_users_chart(virtual_users):
    bar,ax = plt.subplots(figsize=(12,8))
    ax = sns.barplot(x=virtual_users.index, y="variable", data=virtual_users, ci=None, palette="muted",orient='v' )
    #ax.set_title("How long have you been doing performance testing?", fontsize=13)
    ax.set_xlabel ("Virtual Users")
    ax.set_ylabel ("Count")
   

def main():
    FILE_TO_READ = "./Load_Tool_Poll.csv"  # file containing column with tool names seperated by ", ". This is a demo file

    split_string_in_column(FILE_TO_READ)

if __name__ == "__main__":
    main()
