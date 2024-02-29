import pandas as pd
df=pd.read_csv('04_02_2019.csv')

rename_stages = {
    'THORAIPAKK|THURAIPAKK': 'THORAIPAKKAM',
    'ANNA UNIVE': 'ANNA UNIV',
    'MOOTAIKARA': 'M K CHAVADI',
    'SHOZHANGAN|SHOZHINGAN': 'SHOLINGANALLUR',
    'KELAMBAKKA':'KELAMBAKKAM',
    'KOMAN NGR': 'KUMARAN NG',
    'M.K. CHAVA': 'M K CHAVADI',
    'WOMENS POL': 'WPTC',
    'THIRUPPORU|TIRUPPORUR': 'THIRUPORUR',
}
df = df.replace(rename_stages, regex=True)

df['Source'] = df['Source'].str.strip()
df['From Stage'] = df['From Stage'].str.strip()
df['To Stage'] = df['To Stage'].str.strip()
df.to_csv('04-02-19.csv')

#converting transforming into new csv file
df=pd.read_csv('04-02-19.csv')
df=df[df['Schedule Name'].str.contains(r'\b519\b')]
cols=['Schedule Name','Adult','From Stage','To Stage','Trip Start Time','Trip End Time','Source','Destination']
df=df[cols]

df=df[(df['Source']=='T.NAGAR') & (df['Destination']=='THIRUPORUR')]

df['Trip Start Time'] = pd.to_datetime(df['Trip Start Time'], format='%H:%M:%S')
df['Trip End Time'] = pd.to_datetime(df['Trip End Time'], format='%H:%M:%S')

# Filter the rows where trip starts between the given start time and end time
start_time = pd.to_datetime('08:00:00').time()
end_time = pd.to_datetime('09:00:00').time()
df = df[(df['Trip Start Time'].dt.time >= start_time) & 
        (df['Trip Start Time'].dt.time < end_time)]

bus_stages = [
    'T.NAGAR', 'SAIDAPET', 'ANNA UNIV', 'WPTC', 'SRP TOOLS',
    'KANDANCHAV', 'THORAIPAKKAM', 'M K CHAVADI', 'KARAPAKKAM',
    'SHOLINGANALLUR', 'KUMARAN NG', 'CHEMMANCHE', 'NAVALUR',
    'SIPCOT', 'CHURCH', 'PAL. CHEMI', 'HINDUSTAN', 'KELAMBAKKAM',
    'KOMAN NAGAR', 'ENGG', 'CHENGAMMAL', 'KALAVAKKAM','THIRUPORUR'
]

stage_mapping = {stage: i for i, stage in enumerate(bus_stages)}

df['From Stage'] = df['From Stage'].map(stage_mapping)
df['To Stage'] = df['To Stage'].map(stage_mapping)

df.dropna(subset=['From Stage', 'To Stage'], inplace=True)

#create an empty OD matrix
od_matrix = pd.DataFrame(index=range(len(bus_stages)), columns=range(len(bus_stages))).fillna(0)

# populating the matrix 
for index, row in df.iterrows():
    source = int(row['From Stage'])
    destination = int(row['To Stage'])
    adult_count = row['Adult']
    od_matrix.loc[source, destination] += adult_count if not pd.isna(adult_count) else 0

od_matrix['Boarding'] = od_matrix.sum(axis=1)
od_matrix.loc['ALIGHTING'] = od_matrix.sum(axis=0)

#display the entire df
print(od_matrix.to_string())

# Create an empty OD matrix with stage names as indexes and columns
od_matrix = pd.DataFrame(index=bus_stages, columns=bus_stages).fillna(0)

# Populate the matrix 
for index, row in df.iterrows():
    source = bus_stages[int(row['From Stage'])]
    destination = bus_stages[int(row['To Stage'])]
    adult_count = row['Adult']
    od_matrix.loc[source, destination] += adult_count if not pd.isna(adult_count) else 0

# Calculate Boarding and Alighting
od_matrix['Boarding'] = od_matrix.sum(axis=1)
od_matrix.loc['ALIGHTING', :] = od_matrix.sum(axis=0)

# Display the entire OD matrix
od_matrix


