from wrangle import WRANGLEPATH
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np

from numpy import arange

VISPATH = 'visualisations/'

def visualise():
    scatter_diff()
    scatter_plot()
    bar_charts()
    heatmap()
    
# Scatterplot Change

def scatter_diff():
    
    during = pd.read_csv(WRANGLEPATH + 'during_div.csv',encoding = 'ISO-8859-1')
    pre_post = pd.read_csv(WRANGLEPATH + 'prepost_div.csv',encoding = 'ISO-8859-1')
    ses = pd.read_csv(WRANGLEPATH + 'ses.csv',encoding = 'ISO-8859-1')

    during = during.groupby('LGA').sum()
    pre_post = pre_post.groupby('LGA').sum()
    
    during['diff'] = during['total_div_count'] - pre_post['total_div_count']

    plt.scatter(ses.iloc[:,1], during.iloc[:,2], s=10)
    plt.ylabel("Change in Crime Count")
    plt.xlabel("SES Score")
    plt.title("Crime Count Difference between During and Pre/Post Lockdown")
    plt.grid(True)
    plt.savefig(VISPATH + 'Diff_scatter.png')
    plt.close()
    
    return

# Scatterplot

def scatter_plot():
    
    during = pd.read_csv(WRANGLEPATH + 'during_div.csv',encoding = 'ISO-8859-1')
    pre_post = pd.read_csv(WRANGLEPATH + 'prepost_div.csv',encoding = 'ISO-8859-1')
    ses = pd.read_csv(WRANGLEPATH + 'ses.csv',encoding = 'ISO-8859-1')

    during = during.groupby('LGA').sum()
    pre_post = pre_post.groupby('LGA').sum()

    # pre_post
    plt.scatter(ses.iloc[:,1], pre_post.iloc[:,1], s=10, color = 'red')
    plt.ylabel("Total offences")
    plt.xlabel("SES Score")
    
    plt.title("Total offences against SES Score during/pre-post lockdown")
    plt.xlim(850,1150)
    plt.ylim(0,75000)
    plt.grid(True)    
    
    # during scatter
    plt.scatter(ses.iloc[:,1], during.iloc[:,1], s=10, color = 'blue')
    plt.legend(["Pre/Post Lockdown", "During Lockdown"])
    
    plt.savefig(VISPATH + 'scatter_plot.png')
    plt.close()
    
    during = pd.read_csv(WRANGLEPATH + 'during_div.csv',encoding = 'ISO-8859-1')
    pre_post = pd.read_csv(WRANGLEPATH + 'prepost_div.csv',encoding = 'ISO-8859-1')
    ses = pd.read_csv(WRANGLEPATH + 'ses.csv',encoding = 'ISO-8859-1')
    during = during.groupby('LGA').sum()
    pre_post = pre_post.groupby('LGA').sum()

    print("Pearson Correlation (Scatterplot): " + str(during.iloc[:,1].corr(pre_post.iloc[:,1])))

    return


# Bar Chart

# Commented out IPython magic to ensure Python compatibility.
## bar chart
# %matplotlib inline

def bar_charts():
    
    during = pd.read_csv(WRANGLEPATH + 'during_four_class.csv',encoding = 'ISO-8859-1')
    prepost = pd.read_csv(WRANGLEPATH + 'prepost_four_class.csv',encoding = 'ISO-8859-1')
    
    width = 0.4
    ses = ["Low", "Medium Low", "Medium", "High"]
    crime_type = ["A Crimes against the person", " B Property and deception offences", "C Drug offences", \
                  "D Public order and security offences", \
                  "E Justice procedures offences", "F Other offences"]
    
    for i in range(0,6):
        dur_list = during.iloc[i,1:].tolist()
        prepost_list = prepost.iloc[i, 1:].tolist()
        plt.bar(arange(len(dur_list)) - 0.2, dur_list, width)
        plt.bar(arange(len(prepost_list)) + 0.2, prepost_list, width, color = 'red')
        plt.xticks(arange(len(ses)),ses)
        plt.ylabel("Offence Count")
        plt.xlabel("Socioeconomic Divisions")
        plt.title(crime_type[i])
        plt.legend(["During Lockdown", "Pre/Post Lockdown"])
        plt.savefig(VISPATH + crime_type[i] + '.png', bbox_inches='tight')  
        plt.close() 

    return

# Heatmap

def heatmap():
    during = pd.read_csv(WRANGLEPATH + 'during_four_class.csv',index_col=[0])
    prepost = pd.read_csv(WRANGLEPATH + 'prepost_four_class.csv',index_col=[0])
    
    times = [during, prepost]
    title = ['Crime types across different SES levels during lockdown','Crime types across different SES levels prepost lockdown']
    
    for i in range(0,2,1):
         sb.heatmap(times[i],cmap='flare',xticklabels=True)
         plt.ylabel("Crime Types")
         plt.xlabel("Socio-economic Divisions")
         plt.title(title[i])
         plt.savefig(VISPATH + title[i], transparent=False, bbox_inches='tight')
         plt.close()
        
    return