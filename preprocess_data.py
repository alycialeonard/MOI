'''
Prepares datasets for analysis by one-hot encoding demographics and merging demographics to utterances
Inputs: Survey and Utterances CSV files from: https://zenodo.org/record/8032601
Outputs: Prepared survey and utterance CSV files which are inputs to any of the analysis scripts.
Author: Alycia Leonard
Contact: alycia.leonard@eng.ox.ac.uk
Last edited: 2024-03-08
'''

import pandas as pd
import numpy as np

import os

# Get the current working directory and data directory
current_directory = os.getcwd()
data_directory = os.path.join(current_directory, "data")

# Define survey and utterances data filepath
survey_filepath = os.path.join(data_directory, "Siaya_UPV_Survey.csv")
utterances_filepath = os.path.join(data_directory, "Siaya_UPV_Utterances.csv")

# Define paths to save pre-processed survey and utterance data
save_path_survey = os.path.join(data_directory, "Siaya_UPV_Survey_Prepared.csv")
save_path_utterances = os.path.join(data_directory, "Siaya_UPV_Utterances_Prepared.csv")

# Read survey data, ensure that na is only interpreted for empty cells and not "None"
df = pd.read_csv(survey_filepath, skiprows=[0], low_memory=False, keep_default_na=False, na_values=[''])

# Develop one-hot columns based on vulnerability indicators and definitions
df['Youth'] = df['What is your age?'].apply(lambda x: 1 if (36 > x > 0) else (0 if x > 35 else np.nan))
df['Female'] = df['What is your gender?'].apply(lambda x: 1 if x == 'Female' else (0 if x == 'Male' else np.nan))
df['Disabled'] = df['Do you have a disability?'].apply(lambda x: 1 if x == "Yes" else (0 if pd.notna(x) else np.nan))
df['Single'] = df['Marital Status'].apply(lambda x: 1 if x == "Single" else (0 if pd.notna(x) else np.nan))
df['Divorced'] = df['Marital Status'].apply(lambda x: 1 if x == "Divorced" else (0 if pd.notna(x) else np.nan))
df['Widowed'] = df['Marital Status'].apply(lambda x: 1 if x == "Widowed" else (0 if pd.notna(x) else np.nan))
df['No occupation'] = df['What is your current occupation?'].apply(lambda x: 1 if x == "Unemployed" else (0 if pd.notna(x) else np.nan))
df['Low social connectivity'] = df['How well connected do you feel within the community?'].apply(lambda x: 1 if x == "Not connected at all" else (0 if pd.notna(x) else np.nan))
df['Low trust in others'] = df['Generally speaking would say that most people can be trusted or that one cant be too careful in dealing with people?'].apply(lambda x: 1 if "You can't trust anyone" in str(x) else (0 if pd.notna(x) else np.nan))
df['No social support groups'] = df['What community organisation and/or social activity group you are part of? (e.g. church, stokvel, NGO, NPO, Community based organisation, etc.)'].apply(lambda x: 1 if x in ['No', 'None.', 'Not yet.', 'Nothing', 'NONE', 'None'] else (0 if pd.notna(x) else np.nan))
df['No education'] = df['What is the highest level of education have you completed?'].apply(lambda x: 1 if x == "No education" else (0 if pd.notna(x) else np.nan))
df['Low education'] = df['What is the highest level of education have you completed?'].apply(lambda x: 1 if x == "Primary" else (0 if pd.notna(x) else np.nan))
df['Low newspaper'] = df['How often do you read the newspaper?'].apply(lambda x: True if x in ['Never', 'Occasionally'] else (False if pd.notna(x) else np.nan))
df['Low Internet'] = df['How often do you use the internet? (How?)'].apply(lambda x: True if x in ['Never', 'Occasionally'] else (False if pd.notna(x) else np.nan))
df['Low TV'] = df['How often do you watch TV?'].apply(lambda x: True if x in ['Never', 'Occasionally'] else (False if pd.notna(x) else np.nan))
df['Low radio'] = df['How often do you listen to the Radio?'].apply(lambda x: True if x in ['Never', 'Occasionally'] else (False if pd.notna(x) else np.nan))
df['Low information access'] = df['Low radio'] & df['Low newspaper'] & df['Low TV'] & df['Low Internet']
df['Low satisfaction with housing'] = df['Are you happy with the quality of the construction in your house?'].apply(lambda x: 1 if x == "No" else (0 if pd.notna(x) else np.nan))
df['Previous fire'] = df['Have you experienced fire in your home?'].apply(lambda x: True if x == "Yes" else (False if pd.notna(x) else np.nan))
df['Previous flood'] = df['Have you ever experienced flooding in your home?'].apply(lambda x: True if x == "Yes" else (False if pd.notna(x) else np.nan))
df['Previous flood or fire in home'] = df['Previous flood'] | df['Previous fire']
df['No mobile phone'] = df['Which of the following assets do you own?'].apply(lambda x: 1 if (pd.notna(x) and "Mobile phone" not in str(x)) else (0 if pd.notna(x) else np.nan))
df['Low income'] = df['What is the monthly total income of your household (KES)?'].apply(lambda x: 1 if (3253 > x > 0) else (0 if x > 3252 else np.nan))
df['Female-headed household - Main question'] = df['Who would you define as the head of your household?'].apply(lambda x: True if x in ['Grandma', 'Mother', 'My mother', 'Sister', 'Wife', 'Sister'] else (False if pd.notna(x) else np.nan))
df['Female-headed household - Other'] = df['Who is the head of the household?'].apply(lambda x: True if x in ['Grandma', 'Mother', 'My mother', 'Sister', 'Wife', 'Sister'] else (False if pd.notna(x) else np.nan))
df['Female-headed household'] = df['Female-headed household - Main question'] | df['Female-headed household - Other']
df['No electricity access'] = df['What is the main source of electricity in your home?'].apply(lambda x: 1 if x in ['Dry cell battery / torch', 'Phone touch light', 'None'] else (0 if pd.notna(x) else np.nan))
df['Perceived difficulty accessing services'] = df['Do you find it difficult or easy to access this community service?'].apply(lambda x: 1 if "Very Hard" in str(x) else (0 if pd.notna(x) else np.nan))
df['Full dataset'] = df['Interview ID'].apply(lambda x: 1 if pd.notna(x) else np.nan)

# Split the General UPV items by commas and expand into new columns. Then rename those columns and concat them onto df.
split_columns = df['Which 5 items are most important to you in your daily life? Please indicate these in order of importance, starting with the most important'].str.split(',', expand=True)
split_columns.columns = [f'General UPV - Item {i+1}' for i in range(split_columns.shape[1])]
df = pd.concat([df, split_columns], axis=1)

# Split the Climate UPV items by commas and expand into new columns. Then rename those columns and concat them onto df.
split_columns_2 = df['Given the chosen climate event - which 3 items are most useful to you?'].str.split(',', expand=True)
split_columns_2.columns = [f'Climate UPV - Item {i+1}' for i in range(split_columns_2.shape[1])]
df = pd.concat([df, split_columns_2], axis=1)

# Save the processed survey data to a CSV file
df.to_csv(save_path_survey, index=False)

# Read in the utterances data
utterances = pd.read_csv(utterances_filepath, skiprows=[0], low_memory=False)

# Drop all from utterances except the following columns
utterances.drop(utterances.columns.difference(['Extract ID', 'Paragraph ID', 'Interview ID', 'Text', 'Annotations', 'Paragraph Number', 'Question']), axis=1, inplace=True)

# Join utterances to the survey data, including demographic one-hot columns, on the Interview ID
merged = pd.merge(utterances, df, how='left', on='Interview ID')

# Filter the dataframe based on the values in 'Paragraph Number' - 0-4 for general UPV, 5-7 for climate UPV
valid_values = [0, 1, 2, 3, 4]
merged = merged[merged['Paragraph Number'].isin(valid_values)]

# Split the value annotations at ; and expand into new columns. Then rename those columns and concat them onto the merged df.
split_columns = merged['Annotations'].str.split(';', expand=True)
split_columns.columns = [f'Annotation {i+1}' for i in range(split_columns.shape[1])]
merged = pd.concat([merged, split_columns], axis=1)

# Save the processed utternaces data to a CSV file
merged.to_csv(save_path_utterances, index=False)

