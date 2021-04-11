import pandas as pd

dataframe = pd.read_csv('./soc-sign-bitcoinotc.csv', names=['Source','Destination','Weight', 'Time'], usecols=[0,1,2], header=0)
print(dataframe)
