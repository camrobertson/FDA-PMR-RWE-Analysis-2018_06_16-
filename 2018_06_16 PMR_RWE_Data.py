# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 22:59:11 2018

@author: Andrew
"""

import matplotlib.pyplot as plt
import pandas as pd #this is how I usually import pandas
import urllib3
import re
from bs4 import BeautifulSoup
import csv

def df_setup(file_loc):
    PMC_df = pd.read_csv(file_loc, encoding = "ISO-8859-1", delimiter = ',')
    PMC_df['Date_approved'] = PMC_df['NDA_BLA_APPROVAL_DATE'].astype(str).str[:-8] #edits out the time and converts the date from object to string
    PMC_df['Date_approved'] = pd.to_datetime(PMC_df.Date_approved) #converts the date to YYYY-MM-DD format
    PMC_df['Yr_approved'] = PMC_df['Date_approved'].astype(str).str[:4] #gets year only of the approval
    return PMC_df
    

def analysis(df):
    to_graph = df['Yr_approved'].value_counts()
    s = pd.DataFrame(list(to_graph.items()), columns = ['Year', 'Instances'])
    s['Year'] = pd.to_numeric(s['Year'])
    #Counts by year, converts to a dataframe.     
    #Plots.
    #s = s.Year.loc[lambda x: x>1990]
    
    s = s[s['Year'] > 1990]
    plt.bar((s['Year']) , s['Instances'])
    plt.show()
    
    plt.scatter((s['Year']) , s['Instances'])
    plt.show()
    return
#    YR18_df = PMC_df[PMC_df['NDA_BLA_APPROVAL_DATE'].str.contains("2018")]



def main():
    
    file_loc = 'C:/Users/Andrew/Documents/Python_Scripts/FDA_Scripts/FDA Data/pmc/pmc_commitments.txt'
    PMC_df = df_setup(file_loc)
      
    Obs_df = PMC_df[PMC_df['CMT_DESC'].str.contains("observation")]
    Reg_df = PMC_df[PMC_df['CMT_DESC'].str.contains("regist")]
    OpenLab_df = PMC_df[PMC_df['CMT_DESC'].str.contains("open-label")]
    Rand_df = PMC_df[PMC_df['CMT_DESC'].str.contains("randomized")]
    
    analysis(PMC_df)
    analysis(Obs_df)
    analysis(Reg_df)
    analysis(OpenLab_df)
    analysis(Rand_df)
    

    

if __name__ == "__main__":
	main()