'''
Evaluates the percentage of value annotations at each demographic intersection which were each specific value
Inputs: Prepared utterances data file, list of markers (i.e., one-hot columns in data file),
        list of values, minimum sample size (i.e., number of people at an intersection) for data visualisation.
Outputs: Matrices showing the percentage of annotations which were each value for each group (plots and Excel files).
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
utterances_filepath = "data\\Siaya_UPV_Utterances_Prepared.csv"
markers_filepath = 'parameters\\markers.csv'
values_filepath = 'parameters\\values.csv'

# Define path to save results
results_directory = "results\\"

# Define minimum sample size to plot results
minimum_sample_size = 6  # 2% of dataset

# Load list of markers, list of values, utterances data
markers = pd.read_csv(markers_filepath).values.ravel().tolist()
markers.remove('Full dataset')  # Remove this marker in this case as not needed
values = pd.read_csv(values_filepath).values.ravel().tolist()
df = pd.read_csv(utterances_filepath,low_memory=False)

# Create nested dictionary for results
results = {v: {m1: {m2: None for m2 in markers} for m1 in markers} for v in values}

# For each combination of markers:
for m1 in markers:
    for m2 in markers:

        # Grab only the extracts with that vulnerability intersection
        subset = df.loc[(df[m1] == 1) & (df[m2] == 1)]
        # Get the number of unique respondents in that subset
        interviewees = subset['Interview ID'].unique()

        # Check that this subset exceeds the minimum sample size - if it doesn't, don't bother counting it
        if len(interviewees) < minimum_sample_size:
            continue

        # Count the occurrence of values in each annotation column
        # (The annotations are split into up to 6 columns as there can be multiple annotations per extract)
        counts_val1 = subset['Annotation 1'].value_counts()
        counts_val2 = subset['Annotation 2'].value_counts()
        counts_val3 = subset['Annotation 3'].value_counts()
        counts_val4 = subset['Annotation 4'].value_counts()
        counts_val5 = subset['Annotation 5'].value_counts()
        counts_val6 = subset['Annotation 6'].value_counts()
        counts_val7 = subset['Annotation 7'].value_counts()

        # Concatenate these columns into a dataframe called "counts"
        counts = pd.concat([counts_val1, counts_val2, counts_val3, counts_val4, counts_val5, counts_val6, counts_val7]).to_frame()
        # Make the index into a column called "values"
        counts['value'] = counts.index
        # Rename the first column as "count"
        counts.columns.values[0] = 'count'

        # Make dataframe called "count" to hold the sum for each value across all annotation columns
        count = pd.DataFrame(columns=['value', 'count'])

        # Sum across values in "counts" and put the result in "count"
        for v in values:
            s = counts.loc[counts['value'] == v, 'count'].sum()
            data = {"value": v, "count": s}
            count = count.append(data, ignore_index=True)

        # Normalize by dividing by the total number of value annotations, save in column "percent"
        if count['count'].sum() == 0:  # Prevent dividing by zero
            count['percent'] = 0
        else:
            count['percent'] = (count['count'] / count['count'].sum()) * 100

        # Set the index of "count" as the value names
        count.set_index('value', inplace=True)

        # Save the counts for each value for this intersection in the relevant results dict
        for v in values:
            results[v][m1][m2] = count.at[v, 'percent']

# Plot results for each value

for v in values:

    # Get the results for that value as a dataframe
    r = pd.DataFrame.from_dict(results[v]).astype(float)

    # Get rid of weird characters in value name for saving
    replace_chars = [" ", "/", "(", ")", "&", ","]
    value_concat = v
    for char in replace_chars:
        value_concat = value_concat.replace(char, "")

    # Save to Excel
    r.to_excel(results_directory + "value_matrix_" + value_concat + "_percent.xlsx")

    # Create a mask to highlight the diagonal elements
    m = np.eye(len(r), dtype=bool)

    # If there is some data to plot, make a matrix heatmap and save it
    if not r.empty:
        ax = plt.axes()
        sns.heatmap(r, ax=ax, cmap='Reds', annot=True, annot_kws={'size': 8}, fmt='.0f',
                    cbar_kws={'label': '% of annotations which are this value'})

        # Add rectangles to outline the diagonal elements
        for h in range(len(r)):
            for j in range(len(r)):
                if m[h, j]:
                    rect = plt.Rectangle((j, h), 1, 1, fill=False, edgecolor='black', linewidth=1)
                    ax.add_patch(rect)

        ax.set_title("Value matrix (percentage): " + v)
        plt.savefig(results_directory + "value_matrix_" + value_concat + "_percent.png", bbox_inches="tight")
        plt.close()
        plt.clf()
