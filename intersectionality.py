'''
Evaluates the amount of people at each intersection of specified demographic markers in the dataset
Inputs: Prepared survey data file, list of demographic markers (i.e., one-hot columns in data file).
Outputs: Matrix figures of intersectionality of dataset, Excel files with underlying data.
Author: Alycia Leonard
Contact: alycia.leonard@eng.ox.ac.uk
Last edited: 2023-09-05
'''

import pandas as pd
import numpy as np
import warnings
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
warnings.simplefilter(action='ignore', category=FutureWarning)

# Define location of input data
survey_filepath = "data\\Siaya_UPV_Survey_Prepared.csv"
markers_filepath = 'parameters\\markers.csv'

# Define path to save results
results_directory = "results\\"

# Load list of markers, survey data
markers = pd.read_csv(markers_filepath).values.ravel().tolist()
markers.remove('Full dataset')  # Remove this marker in this case as not needed
df = pd.read_csv(survey_filepath, low_memory=False)

# Create nested dictionaries for results
sample_sizes = {m1: {m2: None for m2 in markers} for m1 in markers}
sample_sizes_percent = {m1: {m2: None for m2 in markers} for m1 in markers}
sample_proportions = {m1: {m2: None for m2 in markers} for m1 in markers}

# For each combination of markers:
for m1 in markers:

    # Grab only the rows of the dataset with that vulnerability
    subset1 = df.loc[(df[m1] == 1)]
    # Get the number of unique respondents in that subset
    interviewees1 = subset1['Interview ID'].unique()
    # Get the number of people with marker m1
    len1 = len(interviewees1)

    for m2 in markers:

        # Grab only the rows of the dataset with that vulnerability intersection
        subset = df.loc[(df[m1] == 1) & (df[m2] == 1)]
        # Get the number of unique respondents in that subset
        interviewees = subset['Interview ID'].unique()

        # Store sample size
        sample_sizes[m1][m2] = len(interviewees)
        # Store sample size as a percentage of the whole dataset
        sample_sizes_percent[m1][m2] = len(interviewees)/300
        # Store the percentage of m1 which also has m2
        sample_proportions[m1][m2] = len(interviewees)/len(interviewees1)

# Save sample sizes
s_count = pd.DataFrame.from_dict(sample_sizes).astype(float)
s_percent = pd.DataFrame.from_dict(sample_sizes_percent).astype(float)
s_proportion = pd.DataFrame.from_dict(sample_proportions).astype(float)
s_count.to_excel(results_directory + "intersectionality_count.xlsx")
s_percent.to_excel(results_directory + "intersectionality_percent.xlsx")
s_proportion.to_excel(results_directory + "intersectionality_proportion.xlsx")

# Plot sample sizes

# Create a mask for top triangle in figure (matrix symmetric about diagonal)
mask = np.triu(np.ones_like(s_count.corr()))
np.fill_diagonal(mask, 0)

# Create a mask to highlight the diagonal elements
m = np.eye(len(s_count), dtype=bool)

# Make percent heatmap
fig, ax = plt.subplots(figsize=(12,10))
sns.heatmap(s_percent, ax=ax, cmap='Reds', mask=mask, annot=True, fmt='.0%',
            cbar_kws={'label': 'Percentage of sample at intersection', 'format': ticker.FuncFormatter(lambda x, pos: f'{x:.0%}')})

# Add rectangles to outline the diagonal elements
for i in range(len(s_percent)):
    for j in range(len(s_percent)):
        if m[i, j]:
            rect = plt.Rectangle((j, i), 1, 1, fill=False, edgecolor='black', linewidth=1)
            ax.add_patch(rect)

plt.savefig(results_directory + "intersectionality_percent.png", bbox_inches="tight")
plt.close()
plt.clf()

# Make proportion heatmap
fig, ax = plt.subplots(figsize=(12,10))
sns.heatmap(s_proportion, ax=ax, cmap='Reds', annot=True, fmt='.0%',
            cbar_kws={'label': 'Percentage of the X marker that also has the Y marker',
                      'format': ticker.FuncFormatter(lambda x, pos: f'{x:.0%}')})

plt.savefig(results_directory + "intersectionality_proportion.png", bbox_inches="tight")
plt.close()
plt.clf()

# Make count heatmap
fig, ax = plt.subplots(figsize=(12,10))
sns.heatmap(s_count, ax=ax, cmap='Reds', mask=mask, annot=True, fmt='.0f',
            cbar_kws={'label': 'Number of people in sample at intersection'})

# Add rectangles to outline the diagonal elements
for i in range(len(s_count)):
    for j in range(len(s_count)):
        if m[i, j]:
            rect = plt.Rectangle((j, i), 1, 1, fill=False, edgecolor='black', linewidth=1)
            ax.add_patch(rect)

plt.savefig(results_directory + "intersectionality_count.png", bbox_inches="tight")
plt.close()
plt.clf()
