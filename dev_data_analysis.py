import pandas as pd
data = pd.read_csv("../data.csv")
df = pd.DataFrame([[1,2,3],[4,5,6],[7,8,9],[10,11,12]],\
columns=['A','B','C'])
print(df.loc[ :])
