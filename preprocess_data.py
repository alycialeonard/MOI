'''
Prepares datasets for analysis by one-hot encoding demographics and merging demographics to utterances
Inputs: Survey and Utterances CSV files from: https://zenodo.org/record/8032601
Outputs: Prepared survey and utterance CSV files which are inputs to any of the analysis scripts.
Author: Alycia Leonard
Contact: alycia.leonard@eng.ox.ac.uk
Last edited: 2023-09-05
'''

import pandas as pd
import numpy as np

# Define survey and utterances data filepath
survey_filepath = "data\\Siaya_UPV_Survey.csv"
utterances_filepath = "data\\Siaya_UPV_Utterances.csv"

# Read survey data
df = pd.read_csv(survey_filepath, skiprows=[0], low_memory=False)

# Develop one-hot demographic columns based on conditions
df['Female'] = df['What is your gender?'].apply(lambda x: 1 if x == 'Female' else (0 if x == 'Male' else np.nan))
df['Youth (18-35)'] = df['What is your age?'].apply(lambda x: 1 if (36 > x > 0) else (0 if x > 35 else np.nan))
df['Elders'] = df['What is your age?'].apply(lambda x: 1 if x > 69 else (0 if 0 < x < 70 else np.nan))
df['Unemployed'] = df['What is your current occupation?'].apply(lambda x: 1 if x == "Unemployed" else (0 if pd.notna(x) else np.nan))
df['Single'] = df['Marital Status'].apply(lambda x: 1 if x == "Single" else (0 if pd.notna(x) else np.nan))
df['Divorced'] = df['Marital Status'].apply(lambda x: 1 if x == "Divorced" else (0 if pd.notna(x) else np.nan))
df['Widowed'] = df['Marital Status'].apply(lambda x: 1 if x == "Widowed" else (0 if pd.notna(x) else np.nan))
df['Primary educated'] = df['What is the highest level of education have you completed?'].apply(lambda x: 1 if x == "Primary" else (0 if pd.notna(x) else np.nan))
df['No education'] = df['What is the highest level of education have you completed?'].apply(lambda x: 1 if x == "No education" else (0 if pd.notna(x) else np.nan))
df['Disabled'] = df['Do you have a disability?'].apply(lambda x: 1 if x == "Yes" else (0 if pd.notna(x) else np.nan))
df['Low newspaper'] = df['How often do you read the newspaper?'].apply(lambda x: True if x in ['Never', 'Occasionally'] else (False if pd.notna(x) else np.nan))
df['Low Internet'] = df['How often do you use the internet? (How?)'].apply(lambda x: True if x in ['Never', 'Occasionally'] else (False if pd.notna(x) else np.nan))
df['Low TV'] = df['How often do you watch TV?'].apply(lambda x: True if x in ['Never', 'Occasionally'] else (False if pd.notna(x) else np.nan))
df['Low radio'] = df['How often do you listen to the Radio?'].apply(lambda x: True if x in ['Never', 'Occasionally'] else (False if pd.notna(x) else np.nan))
df['Low information access'] = df['Low radio'] & df['Low newspaper'] & df['Low TV'] & df['Low Internet']
df['Low connection'] = df['How well connected do you feel within the community?'].apply(lambda x: 1 if x == "Not connected at all" else (0 if pd.notna(x) else np.nan))
df['Low trust'] = df['Generally speaking would say that most people can be trusted or that one cant be too careful in dealing with people?'].apply(lambda x: 1 if "You can't trust anyone" in str(x) else (0 if pd.notna(x) else np.nan))
df['Low income'] = df['What is the monthly total income of your household (KES)?'].apply(lambda x: 1 if (3253 > x > 0) else (0 if x > 3252 else np.nan))
df['No electricity access'] = df['What is the main source of electricity in your home?'].apply(lambda x: 1 if x in ['Dry cell battery / torch', 'Phone touch light', 'None'] else (0 if pd.notna(x) else np.nan))
df['Number of females in household'].fillna(0, inplace=True)
df['Number of males in household'].fillna(0, inplace=True)
df['Family size'] = df['Number of females in household'] + df['Number of males in household']
df['Small family'] = df['Family size'].apply(lambda x: 1 if (4 > x > 0) else (0 if x > 3 else np.nan))
df['Female-headed household - Main question'] = df['Who would you define as the head of your household?'].apply(lambda x: True if x in ['Grandma', 'Mother', 'My mother', 'Sister', 'Wife', 'Sister'] else (False if pd.notna(x) else np.nan))
df['Female-headed household - Other'] = df['Who is the head of the household?'].apply(lambda x: True if x in ['Grandma', 'Mother', 'My mother', 'Sister', 'Wife', 'Sister'] else (False if pd.notna(x) else np.nan))
df['Female-headed household'] = df['Female-headed household - Main question'] | df['Female-headed household - Other']
df['Previous fire'] = df['Have you experienced fire in your home?'].apply(lambda x: 1 if x == "Yes" else (0 if pd.notna(x) else np.nan))
df['Previous flood'] = df['Have you ever experienced flooding in your home?'].apply(lambda x: 1 if x == "Yes" else (0 if pd.notna(x) else np.nan))
df['Full dataset'] = df['Interview ID'].apply(lambda x: 1 if pd.notna(x) else np.nan)

# Split the UPVs in by commas and expand into new columns. Then rename those columns and concat them onto df.
split_columns = df['Which 5 items are most important to you in your daily life? Please indicate these in order of importance, starting with the most important'].str.split(',', expand=True)
split_columns.columns = [f'General UPV - Item {i+1}' for i in range(split_columns.shape[1])]
df = pd.concat([df, split_columns], axis=1)

# Save the processed survey data to a CSV file
df.to_csv('data\\Siaya_UPV_Survey_Prepared.csv', index=False)

# Read in the utterances data
utterances = pd.read_csv(utterances_filepath, skiprows=[0], low_memory=False)

# Drop all from utterances except the following columns
utterances.drop(utterances.columns.difference(['Extract ID', 'Paragraph ID', 'Interview ID', 'Text', 'Annotations',
                                               'Paragraph Number', 'Question']), 1, inplace=True)

# Join utterances to the survey data, including demographic one-hot columns, on the Interview ID
merged = pd.merge(utterances, df, how='left', on='Interview ID')

# Filter the dataframe based on the values in 'Paragraph Number' - 0-4 for general UPV, 5-7 for climate UPV
valid_values = [0, 1, 2, 3, 4]
merged = merged[merged['Paragraph Number'].isin(valid_values)]

# Split the annotations at ; and expand into new columns. Then rename those columns and concat them onto the merged df.
split_columns = merged['Annotations'].str.split(';', expand=True)
split_columns.columns = [f'Annotation {i+1}' for i in range(split_columns.shape[1])]
merged = pd.concat([merged, split_columns], axis=1)

# Save the processed utternaces data to a CSV file
merged.to_csv('data\\Siaya_UPV_Utterances_Prepared.csv', index=False)

