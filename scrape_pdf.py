# -*- coding: utf-8 -*-
"""
Created on Thu May 19 17:33:12 2016

@author: pnlawlor
"""

# Load packages
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

csv_loc = 'C:\Users\pnlawlor\GoogleDrive\Research\Projects\Rapporteur\Rapporteur\Data\RapporteurListText.xlsx'

# Load excel file with text from pdf
csv = pd.read_excel(csv_loc)

# Remove date lines
pattern = r'19/05/2016'
idx_dates = csv['Members'].str.contains(pattern)
csv.drop(csv.index[idx_dates],inplace=True)

# Make new dataframe
# Start with rapporteur names
csv_new = pd.DataFrame(csv['Members'][0::3])

# Add country column (which also includes other stuff)
csv_new['Nationality'] = csv.values[2::3,0]

# Extract country name
# Function to do that, will be used with apply()
def extract_country(s):
    country = s.split()[0]
    
    if country == 'United':
        country1 = s.split()[0]
        country2 = s.split()[1]
        country = country1 + ' ' + country2
    elif country == 'Czech':
        country1 = s.split()[0]
        country2 = s.split()[1]
        country = country1 + ' ' + country2
        
    return country
    
# Apply above function to all rows of csv_new
csv_new['Nationality'] = csv_new['Nationality'].apply(extract_country)

# Rename columns to be consistent with the other file
csv_new.columns = ['Name','Nationality']    

# Save file
fname_save = 'C:\Users\pnlawlor\GoogleDrive\Research\Projects\Rapporteur\Rapporteur\Data\MEPNationalityList2.csv'
csv_new.to_csv(fname_save,encoding='utf-8',index=False)