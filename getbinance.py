import pandas as pd
import os
from binance import Client
from dotenv import load_dotenv
from binance.enums import *

load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_SECRET_KEY')

client = Client(API_KEY, API_SECRET)

# Get balances for all assets
balances = client.get_account()["balances"]

# Only show assets with non-zero balances
balances = [asset for asset in balances if float(asset['free']) > 0 or float(asset['locked']) > 0]

# Get balances for all assets in the USDT-margined futures account
futures_balances = client.futures_account_balance()

# Convert the dictionaries to DataFrames
df = pd.DataFrame(balances)

# Convert 'free' and 'locked' columns to floats
df[['free', 'locked']] = df[['free', 'locked']].astype(float)

# Only show assets with non-zero balances
futures_balances = [asset for asset in futures_balances if float(asset['balance']) > 0]

# Convert the dictionaries to DataFrames
df_futures = pd.DataFrame(futures_balances)

# Convert 'balance' column to floats
df_futures['balance'] = df_futures['balance'].astype(float)

# Calculate total balances
df['total'] = df['free'] + df['locked']

# Sort by total balances in descending order
df = df.sort_values(by=['total'], ascending=False)

# Concatenate df_futures to the bottom of df
df_combined = pd.concat([df, df_futures], axis=0)

# Reset the index
df_combined = df_combined.reset_index(drop=True)

# Show the result
print(df_combined)

