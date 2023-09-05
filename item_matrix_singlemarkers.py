'''
Determines the percentage of people with each individual demographic marker who prioritized each item in the UPV game
Inputs: Prepared survey data file, list of markers (i.e., one-hot columns in data file), list of items.
Outputs: Matrix showing the selection of each item across all markers (plot and Excel file).
Author: Alycia Leonard
Contact: alycia.leonard@eng.ox.ac.uk
Last edited: 2023-09-05
'''

import pandas as pd
import numpy as np
import warnings
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
warnings.simplefilter(action='ignore', category=FutureWarning)

# Define location of input data
survey_filepath = "data\\Siaya_UPV_Survey_Prepared.csv"
markers_filepath = 'parameters\\markers.csv'
items_filepath = 'parameters\\items.csv'

# Define path to save results
results_directory = "results\\"

# Load list of markers, list of items, survey data
markers = pd.read_csv(markers_filepath).values.ravel().tolist()
items = pd.read_csv(items_filepath).values.ravel().tolist()
df = pd.read_csv(survey_filepath,low_memory=False)

# Create nested dictionary for results
results = {item: {m1: None for m1 in markers} for item in items}

# For each marker:
for m1 in markers:

    # Grab only the rows of the dataset with that vulnerability
    subset = df.loc[(df[m1] == 1)]

    # Get the number of unique respondents in that subset
    interviewees = subset['Interview ID'].unique()

    # Count the occurrence of items in each UPV column
    counts_item1 = subset['General UPV - Item 1'].value_counts()
    counts_item2 = subset['General UPV - Item 2'].value_counts()
    counts_item3 = subset['General UPV - Item 3'].value_counts()
    counts_item4 = subset['General UPV - Item 4'].value_counts()
    counts_item5 = subset['General UPV - Item 5'].value_counts()

    # Concatenate counts for each UPV column
    counts = pd.concat([counts_item1, counts_item2, counts_item3, counts_item4, counts_item5]).to_frame()
    # Make the index (item name) a column
    counts['item'] = counts.index
    # Rename the first column as count
    counts.columns.values[0] = 'count'

    # Make dataframe called "count" to hold the sum for each item
    count = pd.DataFrame(columns=['item', 'count'])

    # Sum across items in "counts" and put the result in "count"
    for i in items:
        s = counts.loc[counts['item'] == i, 'count'].sum()
        data = {"item": i, "count": s}
        count = count.append(data, ignore_index=True)

    # Normalize by dividing by the total number of people in the subset, save in column "percent"
    count['percent'] = (count['count'] / len(subset))*100

    # Set the index of "count" to be the item names
    count.set_index('item', inplace=True)

    # Save the counts for each item for this intersection in the relevant results dict
    for i in items:
        results[i][m1] = count.at[i, 'percent']

# Get the results as a dataframe
r = pd.DataFrame.from_dict(results).astype(float).transpose()

# Save to Excel
r.to_excel(results_directory + "item_matrix_ALL_percent.xlsx")
# Remove useless items column
r.drop("Items", axis=0, inplace=True)

# If there is some data to plot, make a matrix heatmap and save it
if not r.empty:

    fig, ax = plt.subplots(figsize=(7, 14))
    sns.heatmap(r, ax=ax, cmap='Reds', xticklabels=True, yticklabels=True, vmin=0, vmax=100, annot=True,
                annot_kws={'size': 8}, fmt='.0f', cbar_kws={'label': '% of group who chose the item', 'shrink': 0.33})

    # Get the dimensions of the data
    num_rows, num_cols = r.shape

    # Calculate the coordinates for the rectangle that covers the last column
    rect_x = num_cols - 1
    rect_y = 0
    rect_width = 1
    rect_height = num_rows

    # Draw the rectangle with black outline and no fill
    rect = Rectangle((rect_x, rect_y), rect_width, rect_height, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(rect)

    # Save and close
    plt.savefig(results_directory + "item_matrix_ALL_percent.png", bbox_inches="tight")
    plt.close()
    plt.clf()
