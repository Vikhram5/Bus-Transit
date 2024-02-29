# 519 bus counts w.r.t. Start time
import pandas as pd
df=pd.read_csv('519.csv')

cols=['Schedule Name','Trip Start Time','Source','Destination']
buses_df=df[cols]
#transform to another csv file
buses_df.to_csv('bus_counts.csv')


df=pd.read_csv('bus_counts.csv')
# Hour time 
df['Trip Start Time'] = pd.to_datetime(df['Trip Start Time'], format='%H:%M:%S')
df['Hour']=df['Trip Start Time'].dt.hour

cols=['Schedule Name','Hour']
df_final=df[cols]
df_final.head()

# Bus counts
bus_df=df.groupby('Hour')['Schedule Name'].count().reset_index()
bus_df.columns=['Hour','Bus Count']
bus_df

print(bus_df['Bus Count'].sum())

#transform to final csv
bus_df.to_csv('519_bus_count.csv')





