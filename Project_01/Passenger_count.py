import pandas as pd
df=pd.read_csv('04-02-19.csv')

df=df[df['Schedule Name'].str.contains(r'\b519\b')]

df=df[(df['Source']=='T.NAGAR') & (df['Destination']=='THIRUPORUR')]
df['Trip Start Time'] = pd.to_datetime(df['Trip Start Time'], format='%H:%M:%S')
df['Trip End Time'] = pd.to_datetime(df['Trip End Time'], format='%H:%M:%S')

cols=['Schedule Name','Adult','Trip Start Time','Trip End Time','Source','Destination']
df=df.sort_values(by='Trip Start Time')
df=df[cols]

df['Duration'] = df['Trip End Time'] - df['Trip Start Time']
df['Trip Start Time'] = df['Trip Start Time'].dt.time
df['Trip End Time'] = df['Trip End Time'].dt.time
df['Duration'] = df['Duration'].apply(lambda x: str(x).split()[-1])
df['Passenger Count'] = df.groupby(['Schedule Name', 'Trip Start Time', 'Trip End Time'])['Adult'].transform('sum')

df=df.drop(columns=['Adult'])
#remove duration with error values 
df = df[~df['Duration'].str.contains('+', regex=False)]
df = df[(df['Duration'] != '00:00:00') & (df['Duration'] != '00:01:00')]

#drop duplicate rows
df=df.drop_duplicates()
print(df.to_string())

df.to_excel('passenger_count.xlsx')

