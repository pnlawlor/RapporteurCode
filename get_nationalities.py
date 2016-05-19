# -*- coding: utf-8 -*-
"""
Created on Wed May 18 23:13:36 2016

@author: pnlawlor
"""
# Load packages
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz


# Load data
csv_loc = 'C:\Users\pnlawlor\GoogleDrive\Research\Projects\Rapporteur\Rapporteur\Data\DataCleaned.csv'
data_csv = pd.read_csv(csv_loc) 

# Load the variable list file
var_loc = 'C:\Users\pnlawlor\GoogleDrive\Research\Projects\Rapporteur\Rapporteur\Data\VariableList.xlsx'
var_csv = pd.read_excel(var_loc,sheetname='Sheet3')

# Load the nationalities file
nat_loc = 'C:\Users\pnlawlor\GoogleDrive\Research\Projects\Rapporteur\Rapporteur\Data\MEPNationalityList.xlsx'
nat_csv = pd.read_excel(nat_loc)
nat_csv.drop('Year : Party',axis=1,inplace=True)
nat_csv.dropna(how='any',inplace=True)

# Get unique countries in nationalities file
nats = nat_csv.Nationality.unique()
nats.sort() # Alphabetize
raps = nat_csv.Name

# Get list of rapporteur variables
rap_vars = var_csv['Rapporteurs'] 
rap_vars_cleaned = [v for v in rap_vars if str(v) != 'nan'] # get rid of nans

# Add columns to big data file, one for each country. This will represent "there was at least one rap from this country"
for i in range(len(nats)):
    country = nats[i]
    temp = pd.Series(np.empty(data_csv.values.shape[0]), index = data_csv.index)
    data_csv.insert(4+i,country,temp)
    data_csv[country] = np.nan
    
# Loop through each rap listed in the file

fuzzy_threshold = 65 # How similar the two names have to be to be counted as "the same". I chose this with a little bit of trial and error. Far from perfect.

def isnotnanstr(s):
    return str(s)!='nan'

# For each rap
for i in range(nat_csv.values.shape[0]):
    print(nat_csv.values[i,0] + ' from ' + nat_csv.values[i,1])
    # For each rap_var
    for rap_var in rap_vars_cleaned:
        
        # Find ~nan
        idx_good = data_csv[rap_var].apply(isnotnanstr)
        
        # Apply fuzzy wuzzy (fuzzy text matching; order-independent)
        temp = data_csv[rap_var][idx_good].apply(
                                    fuzz.token_sort_ratio,
                                    args=(nat_csv.values[i,0],))
        
        # Find rows where similarity score > threshold
        temp2 = temp > fuzzy_threshold
        
        if np.sum(temp2) > 0:
            print rap_var
        
        # Set values for corresponding column
        idx_write = [x for x in temp2.index if x==True]
        data_csv.set_value(idx_write,nat_csv.values[i,1],True)
        
# Write cleaned csv
fname_write = 'C:\Users\pnlawlor\GoogleDrive\Research\Projects\Rapporteur\Rapporteur\Data\DataCleaned_countries.csv'
data_csv.to_csv(fname_write)
        


