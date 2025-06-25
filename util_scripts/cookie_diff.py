import pandas as pd
import ast
# File path
file_path1 = 'acceptance.csv' # output files from parse_cookies_category_wise.py
file_path2='rejection.csv'
#file_path3= 'withdrawal_not_possible.csv'
# Read the CSV file into a DataFrame
df1 = pd.read_csv(file_path1)
df2 = pd.read_csv(file_path2)
#df3 = pd.read_csv(file_path3)
# Display the DataFrame
print(df1.keys())
print(df2.keys())
#print(df3.keys())

#ll=list(df3['Website'])

l=[]
i=0
for value1, value2 in zip(df1['Count-Ana'], df2['Count-Ana']): 
    i=i+1
    print(f"Value from df1: {value1}, Value from df2: {value2}")  
    #print(df1['Website'][i])
    try:
        acceptance= value1
        revocation= value2
        if acceptance < revocation:
            l.append(df1['Website'][i])
    except Exception as e:
        print("Error:",e)
        continue
        
print(l)
print(len(l))
