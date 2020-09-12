# -*- coding: utf-8 -*-
"""
    IDBank2YNAB
    ~~~~~~~~~~~

    Script to convert IDBank statements to YNAB format

    Assumes you've read this 🙃

    Usage:
        $ python IDBank2YNAB.py input.xlsx output.csv
"""

import sys
import pandas as pd

# read from excel and ignore uneccessary top rows
statement = pd.read_excel(sys.argv[1])[10:]

# get rid of \n and \t chars
statement = statement.replace(['\n', '\t'], '', regex = True)

# turn first row into pd header and drop last 2 rows
statement = statement.rename(columns = statement.iloc[0]).drop(statement.index[0])[:-2]

# get rid of rows with NaN doc number
statement = statement[statement['Document number'].notna()]

# reformat date into DD/MM/YYYY
statement['Dabit'] = statement['Dabit'].str[:-8] + '20' + statement['Dabit'].str[-8:-6]


# Create new pd df from those 5 columns
new_statement = statement[['Dabit', 'Name', 'Reason', 'Date', 'Credit']]

# Rename columns to YNAB format
new_statement.columns = ['Date', 'Payee', 'Memo', 'Outflow', 'Inflow']

# output to CSV from cli arg
new_statement.to_csv(sys.argv[2])

print('Done!')