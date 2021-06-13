# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

import holoviews as hv
hv.extension('bokeh')

import warnings
warnings.filterwarnings("ignore")
 
 
def extract_data(file_name):
    
    STATUS = True #doggle chart generation ON/OFF
    
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
        
        #Get experience
        experience = Counter(tools_df['experience'])
        experience_list = pd.DataFrame(experience.items())
        experience_list.columns = ['experience','count']
    
        
        #Get experience by country
        sankey = tools_df.groupby(["experience", "country"]).size().reset_index(name="Time")
        experience_by_country(sankey)
        
       
        #Get virtual users load tested to in current engagement
        virtual_users = Counter(tools_df['virtual_users'])
        virtual_users_list = pd.DataFrame(virtual_users.items())
        virtual_users_list.columns = ['virtual users','count']
        virtual_users_chart(virtual_users_list)
        
        
        if STATUS == True:
            tools_used_chart(tools_used_table.T)
            current_tool_chart(current_tool_table.T)
            fav_tool_chart(fav_tool_table.T) 
            country_chart(country_list)
            current_industry_chart(current_industry_list)
            title_word_chart(tools_df['title'])
            experience_chart(experience_list)
        
    except Exception as e:
        print(e)

def autopct(pct):
    return ('%1.f%%' % pct) if pct > 1 else ''

def experience_by_country(expr_by_country):
    
    custom_dict = {'< 1 year': 0, '1-5 years': 1, '6-10 years': 2, '11-15 years': 3, '> 15 years': 4}
    
    expr_by_country['experience'] = pd.Categorical(expr_by_country['experience'], categories=sorted(custom_dict, key=custom_dict.get), ordered=True)
    
    expr_by_country.sort_values('experience',inplace=True, ignore_index=True)
        
    test = expr_by_country.reindex()

    figure = hv.Sankey(test)
    
    figure.opts(cmap='Colorblind',label_position='left',
                                  edge_color='country', edge_line_width=0,
                                  node_alpha=1.0, node_width=40, node_sort=True,
                                  width=1000, height=1000, bgcolor="snow",
                                  title="Experience By Country")
    
    hv.save(figure, 'graph.html')
    
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
    custom_dict = {'< 1 year': 0, '1-5 years': 1, '6-10 years': 2, '11-15 years': 3, '> 15 years': 4}
    
    experience['experience'] = pd.Categorical(experience['experience'], categories=sorted(custom_dict, key=custom_dict.get), ordered=True)
    
    experience.sort_values('experience',inplace=True, ignore_index=True)
    bar,ax = plt.subplots(figsize=(10,6))
    ax = sns.barplot(x="experience", y="count", data=experience, ci=None, palette="muted",orient='v' )
    #ax.set_title("How long have you been doing performance testing?", fontsize=13)
    ax.set_xlabel ("Years of Experience")
    ax.set_ylabel ("Count")
    
def virtual_users_chart(virtual_users):
    custom_dict = {'0 - 100 VUs': 0, '100 - 999 VUs': 1, '1,000 -  2,499 VUs': 2, '2,500 - 4,999 VUs': 3, '5,000 - 9,999 VUs': 4, '10,000 - 49,999 VUs': 5, '> 50,000 VUs': 6}
    
    virtual_users['virtual users'] = pd.Categorical(virtual_users['virtual users'], categories=sorted(custom_dict, key=custom_dict.get), ordered=True)  
    virtual_users.sort_values('virtual users',inplace=True, ignore_index=True)
    bar,ax = plt.subplots(figsize=(14,6))
    ax = sns.barplot(x="count", y="virtual users", data=virtual_users, ci=None, palette="muted",orient='h' )
    ax.set_xlabel ("Count")
    ax.set_ylabel ("Virtual Users")
    for rect in ax.patches:
        ax.text (rect.get_width(), rect.get_y() + rect.get_height() / 2,"%d"% rect.get_width(), weight='bold' )
   

def main():
    FILE_TO_READ = "./Load_Tool_Poll.csv"  # file containing column with tool names seperated by ", ". This is a demo file

    extract_data(FILE_TO_READ)

if __name__ == "__main__":
    main()
