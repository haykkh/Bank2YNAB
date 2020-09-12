# -*- coding: utf-8 -*-
"""
    Ineco2YNAB
    ~~~~~~~~~~

    Script to convert InecoBank statements to YNAB format

    Assumes to have read this 🙃

    Usage:
        $ python Ineco2YNAB.py input.csv output.csv
"""

import sys
import pandas as pd

# read from csv and ignore uneccessary top rows
statement = pd.read_csv(sys.argv[1], encoding='utf-16')[8:]

# turn first row into pd header and drop last row
statement = statement.rename(columns = statement.iloc[0]).drop(statement.index[0])[:-1]


# Create new pd df from those 5 columns
new_statement = statement[['Date', 'Receiver/Payer', 'Details', 'Expense', 'Income']]

# Rename columns to YNAB format
new_statement.columns = ['Date', 'Payee', 'Memo', 'Outflow', 'Inflow']

# output to CSV from cli arg
new_statement.to_csv(sys.argv[2])

print('Done!')
