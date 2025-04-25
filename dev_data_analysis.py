import pandas as pd
df = pd.read_csv('data.csv') #a table
pd.set_option('display.max_columns', 20) #show 20 columns
pd.set_option('display.max_rows', 20) #show 20 rows
print(df.info()) 
print(df.head()) #first 5 rows