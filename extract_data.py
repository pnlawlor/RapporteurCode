# -*- coding: utf-8 -*-
"""
Created on Sun May 08 21:39:45 2016

@author: pnlawlor
"""

# Load packages

import pandas as pd
import numpy as np

# Specify locations of files
data_loc = 'C:\Users\pnlawlor\Downloads\prlx-v05-management01\prlx-v05-management01.csv'
vars_loc = 'C:\Users\pnlawlor\GoogleDrive\Research\Projects\Rapporteur\Rapporteur\Data\VariableList.xlsx'

# Load files
data_csv = pd.read_csv(data_loc) # data file
vars_csv = pd.read_excel(vars_loc,sheetname='Sheet3') # list of variables to keep

# Clean up list of variables to keep
vars_to_keep = vars_csv.values.flatten() # 2d table to 1d list, "flatten"
vars_to_keep_cleaned = [v for v in vars_to_keep if str(v) != 'nan'] # get rid of nans

# Get rid of unneccessary columns
data_csv = data_csv[vars_to_keep_cleaned] # keep only the columns desired

# Write cleaned csv
fname_write = 'C:\Users\pnlawlor\GoogleDrive\Research\Projects\Rapporteur\Rapporteur\Data\DataCleaned'
data_csv.to_csv(fname_write)