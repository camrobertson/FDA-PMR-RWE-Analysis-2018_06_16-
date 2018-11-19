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
    
    s = s[s['Year'] > 1998]
    plt.bar((s['Year']) , s['Instances'])
    plt.ylim(0, 45)
    plt.show()
    
    plt.scatter((s['Year']) , s['Instances'])
    plt.show()
    return s
#    YR18_df = PMC_df[PMC_df['NDA_BLA_APPROVAL_DATE'].str.contains("2018")]


#merge datasets into single
#def merge()

def status_count(df):
    splits = df['CMT_STATUS'].value_counts()
    splits = pd.DataFrame(list(splits.items()), columns = ['STATUS', 'Instances'])
    return(splits)

def center_count(df):
    subpart = df['CDER_OR_CBER'].value_counts()
    subpart = pd.DataFrame(list(subpart.items()), columns = ['SUBPART', 'Instances'])
    return(subpart)

def subpart_count(df):
    subpart = df['SUBPART_FLAG'].value_counts()
    subpart = pd.DataFrame(list(subpart.items()), columns = ['SUBPART', 'Instances'])
    return(subpart)


def subpart_split(Obs_df, Reg_df, OpenLab_df, Rand_df):
    fObs_df = subpart_count(Obs_df)
    fObs_df.columns = ['FLAG', 'Obs']

    fReg_df = subpart_count(Reg_df)
    fReg_df.columns = ['FLAG', 'Reg']

    fOPL_df = subpart_count(OpenLab_df)
    fOPL_df.columns = ['FLAG', 'OPL']

    fRan_df = subpart_count(Rand_df)
    fRan_df.columns = ['FLAG', 'Ran']
    
    fmaster_df = pd.merge(fObs_df, fReg_df, how = 'outer', on = 'FLAG')
    fmaster_df = pd.merge(fmaster_df, fOPL_df, how = 'outer', on = 'FLAG')
    fmaster_df = pd.merge(fmaster_df, fRan_df, how = 'outer', on = 'FLAG')
    print(fmaster_df)
    return(fmaster_df)


def center_split(Obs_df, Reg_df, OpenLab_df, Rand_df):
    cObs_df = center_count(Obs_df)
    cObs_df.columns = ['CENTER', 'Obs']

    cReg_df = center_count(Reg_df)
    cReg_df.columns = ['CENTER', 'Reg']

    cOPL_df = center_count(OpenLab_df)
    cOPL_df.columns = ['CENTER', 'OPL']

    cRan_df = center_count(Rand_df)
    cRan_df.columns = ['CENTER', 'Ran']
    
    cmaster_df = pd.merge(cObs_df, cReg_df, how = 'outer', on = 'CENTER')
    cmaster_df = pd.merge(cmaster_df, cOPL_df, how = 'outer', on = 'CENTER')
    cmaster_df = pd.merge(cmaster_df, cRan_df, how = 'outer', on = 'CENTER')
    print(cmaster_df)
    return(cmaster_df)


def status_split(Obs_df, Reg_df, OpenLab_df, Rand_df):
    sObs_df = status_count(Obs_df)
    sObs_df.columns = ['Status', 'Obs']

    sReg_df = status_count(Reg_df)
    sReg_df.columns = ['Status', 'Reg']

    sOPL_df = status_count(OpenLab_df)
    sOPL_df.columns = ['Status', 'OPL']

    sRan_df = status_count(Rand_df)
    sRan_df.columns = ['Status', 'Ran']
    
    smaster_df = pd.merge(sObs_df, sReg_df, how = 'outer', on = 'Status')
    smaster_df = pd.merge(smaster_df, sOPL_df, how = 'outer', on = 'Status')
    smaster_df = pd.merge(smaster_df, sRan_df, how = 'outer', on = 'Status')
    print(smaster_df)
    return(smaster_df)
    

def year_split(Obs_df, Reg_df, OpenLab_df, Rand_df):
    #yPMC_df = analysis(PMC_df)
    yObs_df = analysis(Obs_df)
    yObs_df.columns = ['Year', 'Obs']
    
    yReg_df = analysis(Reg_df)
    yReg_df.columns = ['Year', 'Reg']
    
    yOpl_df = analysis(OpenLab_df)
    yOpl_df.columns = ['Year', 'OPL']
    
    yRan_df = analysis(Rand_df)  
    yRan_df.columns = ['Year', 'Ran']
    
    #ymaster_df = pd.merge(, yObs_df, on = 'Year')
    ymaster_df = pd.merge(yObs_df, yReg_df, how = 'outer', on = 'Year')
    ymaster_df = pd.merge(ymaster_df, yOpl_df, how = 'outer', on = 'Year')
    ymaster_df = pd.merge(ymaster_df, yRan_df, how = 'outer',on = 'Year')
    
    ymaster_df = ymaster_df.sort_values('Year')
    ymaster_df = ymaster_df.reset_index()
    ymaster_df = ymaster_df[['Year', 'Obs', 'Reg', 'OPL', 'Ran']]
    
    plt.bar(ymaster_df['Year'], ymaster_df['Obs'])
    print(ymaster_df)
    return(ymaster_df)
    

def main():
    
    file_loc = 'C:/Users/Andrew/Documents/Python_Scripts/FDA_Scripts/FDA Data/pmc/pmc_commitments.txt'
    PMC_df = df_setup(file_loc)
      
    Obs_df = PMC_df[PMC_df['CMT_DESC'].str.contains("observation")]
    Reg_df = PMC_df[PMC_df['CMT_DESC'].str.contains("regist")]
    OpenLab_df = PMC_df[PMC_df['CMT_DESC'].str.contains("open-label")]
    Rand_df = PMC_df[PMC_df['CMT_DESC'].str.contains("randomized")]
    #Cohort_df = PMC_df[PMC_df['CMT_DESC'].str.contains("cohort")]
    #surveillance_df = PMC_df[PMC_df['CMT_DESC'].str.contains("surveillance")]
    #real_world_df = PMC_df[PMC_df['CMT_DESC'].str.contains("Real World")]

    
    #Status split
    smaster_df = status_split(Obs_df, Reg_df, OpenLab_df, Rand_df)
       
    #yPMC_df = analysis(PMC_df)
    ymaster_df = year_split(Obs_df, Reg_df, OpenLab_df, Rand_df)
    
    #Flag Subpart Split
    fmaster_df = subpart_split(Obs_df, Reg_df, OpenLab_df, Rand_df)

    #Center Split
    cmaster_df = center_split(Obs_df, Reg_df, OpenLab_df, Rand_df)

    writer = pd.ExcelWriter('C:/Users/Andrew/Documents/Python_Scripts/FDA_Scripts/FDA Data/pmc/PMC_data.xlsx')
    ymaster_df.to_excel(writer,'Study_type_by_year')
    smaster_df.to_excel(writer, 'Study_type_by_status')
    fmaster_df.to_excel(writer, 'Study_by_Flag')
    cmaster_df.to_excel(writer, 'Study_by_Center')
    writer.save()


if __name__ == "__main__":
	main()