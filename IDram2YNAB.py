# -*- coding: utf-8 -*-
"""
    IDramk2YNAB
    ~~~~~~~~~~~

    Script to convert (old) IDram wallet statements to YNAB format

    Assumes you've read this 🙃

    You will need to convert the cells in the *.xls from functions to values

    Usage:
        $ python IDram2YNAB.py input.xls output.csv
"""

import sys
import pandas as pd

# read from excel and ignore uneccessary top rows
statement = pd.read_excel(sys.argv[1])[15:]

# get rid of NaN rows
statement = statement[statement['Unnamed: 5'].notna()]

# Set column headers
statement.columns = ['Date', 'Amount', 'Outflow', 'Inflow', 'Fees', 'Memo', 'Remaining']


## Add 'Fees' into their own rows after each transaction
# Copy statement's rows that contain fees
fees = statement[statement['Fees'] != 0].copy()

# Add the 'Fees' into 'Outflow' column
fees['Outflow'] = fees['Fees']

# Set the 'Memo's
fees['Memo'] = 'IDram Fee'

# Add back to statement and sort
statement = statement.append(fees).sort_index()

# Zero out 'Fees' column to `look nice`
statement['Fees'] = 0

# reformat date into DD/MM/YYYY
statement['Date'] = statement['Date'].str[:-6]

# Create new pd df from those 5 columns
new_statement = statement[['Date', 'Memo', 'Memo', 'Outflow', 'Inflow']]

# Rename columns to YNAB format
new_statement.columns = ['Date', 'Payee', 'Memo', 'Outflow', 'Inflow']

# output to CSV from cli arg
new_statement.to_csv(sys.argv[2])

print('Done!')