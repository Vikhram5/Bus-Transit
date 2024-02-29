import pandas as pd
df=pd.read_csv('04_02_2019.csv')

#data replacing
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
cols=['Schedule Name','Adult','From Stage','To Stage','Trip Start Time','Trip End Time','Source','Destination']
df=df[cols]

name=input("Enter Schedule Name: ")
source=input("Enter Source: ")
destination=input("Enter Destination: ")
start_time=input("Enter Trip Start Time ")
end_time=input("Enter Trip End Time ")

df=df[df['Schedule Name']==name]
df=df[(df['Source'] == source) & (df['Destination']==destination)]
df=df[(df['Trip Start Time']==start_time) & (df['Trip End Time']==end_time)]

cols=['From Stage','To Stage','Adult']
df=df[cols]

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










