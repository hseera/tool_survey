# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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
        
        tools_used_chart(tools_used_table.T)
        current_tool_chart(current_tool_table.T)
        fav_tool_chart(fav_tool_table.T)
        
        
    except Exception as e:
        print(e)

def autopct_more_than_1(pct):
    return ('%1.f%%' % pct) if pct > 1 else ''

def tools_used_chart(tools_used):
    
    bar,ax = plt.subplots(figsize=(10,10))
    ax = sns.barplot(x="variable", y=tools_used.index, data=tools_used, ci=None, palette="muted",orient='h' )
    ax.set_title("In past three years, for your work, which load test tools have you used the most?", fontsize=13)
    ax.set_xlabel ("Count")
    ax.set_ylabel ("Tool")
    for rect in ax.patches:
        ax.text (rect.get_width(), rect.get_y() + rect.get_height() / 2,"%d"% rect.get_width(), weight='bold' )

def current_tool_chart(current_tool):
    bar,ax = plt.subplots(figsize=(10,10))
    ax = sns.barplot(x="variable", y=current_tool.index, data=current_tool, ci=None, palette="muted",orient='h' )
    ax.set_title("Which load test tool are you using in your current engagement/job?", fontsize=13)
    ax.set_xlabel ("Count")
    ax.set_ylabel ("Tool")
    for rect in ax.patches:
        ax.text (rect.get_width(), rect.get_y() + rect.get_height() / 2,"%d"% rect.get_width(), weight='bold' )

def fav_tool_chart(fav_tool):
    bar,ax = plt.subplots(figsize=(10,10))
    ax = sns.barplot(x="variable", y=fav_tool.index, data=fav_tool, ci=None, palette="muted",orient='h' )
    ax.set_title("Which is your favorite load test tool(/load test platform)?", fontsize=13)
    ax.set_xlabel ("Count")
    ax.set_ylabel ("Tool")
    for rect in ax.patches:
        ax.text (rect.get_width(), rect.get_y() + rect.get_height() / 2,"%d"% rect.get_width(), weight='bold' )


#def print_data(t1, t2, t3):
#    
#    #fig, ax = plt.subplots(2,2)
#    #ax = ax.flatten()
#    fig, axes = plt.subplots(2, 2, figsize=(10, 10), sharey=False)
#    
#    bar,ax = plt.subplots(figsize=(10,10))
#    ax = sns.barplot(ax=axes[0,0], x="variable", y=t1.index, data=t1, ci=None, palette="muted",orient='h' )
#    ax.set_title("In past three years, for your work, which load test tools have you used the most?", fontsize=13)
#    ax.set_xlabel ("Count")
#    ax.set_ylabel ("Tool")
#    for rect in ax.patches:
#        ax.text (rect.get_width(), rect.get_y() + rect.get_height() / 2,"%d"% rect.get_width(), weight='bold' )
#    #sns.histplot(data=t1, y="all", x='variable')
#    
#    fig.tight_layout(pad=2)
#    print(t1)
#    #sns.histplot(data=t2, y="value", x='variable')
#    #sns.histplot(data=t3, y="value", x='variable')
#    print(t2)
#    print(t3)
#           

def main():
    FILE_TO_READ = "./Load_Tool_Poll.csv"  # file containing column with tool names seperated by ", ". This is a demo file

    split_string_in_column(FILE_TO_READ)

if __name__ == "__main__":
    main()
