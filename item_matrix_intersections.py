'''
Determines the percentage of people at each intersection who prioritized each item in the UPV game
Inputs: Prepared survey data file, list of demographic markers (i.e., one-hot columns in data file),
        list of items, minimum sample size (i.e., number of people at an intersection) for data visualisation.
Outputs: Matrices showing the selection of each item across all intersections (plots and Excel files).
Author: Alycia Leonard
Contact: alycia.leonard@eng.ox.ac.uk
Last edited: 2023-09-05
'''

import pandas as pd
import numpy as np
import warnings
import seaborn as sns
import matplotlib.pyplot as plt
warnings.simplefilter(action='ignore', category=FutureWarning)

# Define location of input data
survey_filepath = "data\\Siaya_UPV_Survey_Prepared.csv"
markers_filepath = 'parameters\\markers.csv'
items_filepath = 'parameters\\items.csv'

# Define path to save results
results_directory = "results\\"

# Define minimum sample size to plot results
minimum_sample_size = 6  # 2% of dataset

# Load list of markers, list of items, survey data
markers = pd.read_csv(markers_filepath).values.ravel().tolist()
markers.remove('Full dataset')  # Remove this marker in this case as not needed
items = pd.read_csv(items_filepath).values.ravel().tolist()
df = pd.read_csv(survey_filepath, low_memory=False)

# Create nested dictionary for results
results = {item: {m1: {m2: None for m2 in markers} for m1 in markers} for item in items}

# For each combination of markers:
for m1 in markers:
    for m2 in markers:

        # Grab only the rows of the dataset with that vulnerability intersection
        subset = df.loc[(df[m1] == 1) & (df[m2] == 1)]
        # Get the number of unique respondents in that subset
        interviewees = subset['Interview ID'].unique()

        # Check that this subset exceeds the minimum sample size - if it doesn't, don't bother counting it
        if len(interviewees) < minimum_sample_size:
            continue

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
            results[i][m1][m2] = count.at[i, 'percent']

# Plot results for each item

for i in items:

    # Get the results for that item as a dataframe
    r = pd.DataFrame.from_dict(results[i]).astype(float)

    # Get rid of weird characters in value name for saving
    replace_chars = [" ", "/", "(", ")", "&", ","]
    item_concat = i
    for char in replace_chars:
        item_concat = item_concat.replace(char, "")

    # Save to Excel
    r.to_excel(results_directory + "item_matrix_" + item_concat + "_percent.xlsx")

    # Create a mask to highlight the diagonal elements
    m = np.eye(len(r), dtype=bool)

    # If there is some data to plot, make a matrix heatmap and save it
    if not r.empty:
        ax = plt.axes()
        g = sns.heatmap(r, ax=ax, cmap='Reds', vmin=0, vmax=100, annot=True, annot_kws={'size': 8}, fmt='.0f',
                        cbar_kws={'label': '% of group who chose the item'})

        # Add rectangles to outline the diagonal elements
        for h in range(len(r)):
            for j in range(len(r)):
                if m[h, j]:
                    rect = plt.Rectangle((j, h), 1, 1, fill=False, edgecolor='black', linewidth=1)
                    ax.add_patch(rect)

        ax.set_title("Item matrix: " + i)
        plt.savefig(results_directory + "item_matrix_" + item_concat + "_percent.png", bbox_inches="tight")
        plt.close()
        plt.clf()


