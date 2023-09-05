'''
Analyses the amount of people with each demographic marker which chose each item as a priority
Inputs: Prepared survey data, list of markers (i.e., one-hot columns in data file).
Outputs: Plots of item prioritisation (normalized and count-based), item prioritisation Excel files.
Author: Alycia Leonard
Contact: alycia.leonard@eng.ox.ac.uk
Last edited: 2023-09-05
'''

import pandas as pd
import warnings
import matplotlib.pyplot as plt
warnings.simplefilter(action='ignore', category=FutureWarning)

# Define location of input data
survey_filepath = "data\\Siaya_UPV_Survey_Prepared.csv"
markers_filepath = 'parameters\\markers.csv'

# Define path to save results
results_directory = "results\\"

# Load list of markers and survey data
markers = pd.read_csv(markers_filepath).values.ravel().tolist()
df = pd.read_csv(survey_filepath, low_memory=False)

# Loop through each marker in the list
for m in markers:

    # Grab only the rows of the dataset with that vulnerability
    subset = df.loc[(df[m] == 1)]

    # Count the occurrence of items in each general UPV column
    counts_item1 = subset['General UPV - Item 1'].value_counts()
    counts_item2 = subset['General UPV - Item 2'].value_counts()
    counts_item3 = subset['General UPV - Item 3'].value_counts()
    counts_item4 = subset['General UPV - Item 4'].value_counts()
    counts_item5 = subset['General UPV - Item 5'].value_counts()

    # Dataframe to hold summed results
    count = pd.DataFrame(columns=['item', 'count'])

    # Concatenate frames for each UPV column
    counts = pd.concat([counts_item1, counts_item2, counts_item3, counts_item4, counts_item5]).to_frame()
    # Make the index (item name) a column
    counts['item'] = counts.index
    # Rename the first column as count
    counts.columns.values[0] = 'count'
    # Get the unique items
    items = counts['item'].unique()

    # Sum across items
    for i in items:
        s = counts.loc[counts['item'] == i, 'count'].sum()
        data = {"item": i, "count": s}
        count = count.append(data, ignore_index=True)

    # Sort items in descending order
    count = count.sort_values(by=['count'], ascending=False)

    # Normalize by dividing by the total number of people in the subset
    count['percent'] = (count['count'] / len(subset))*100

    # Save the counts data to excels
    count.to_excel(results_directory + 'item_plot_' + m + '_percent.xlsx')

    # # Plot counts
    # fig, ax = plt.subplots()
    # count.plot(x='item', y='count', kind='bar', figsize=(10, 6), rot=90, ax=ax, legend=False)
    # plt.xlabel("Item")
    # plt.ylabel("Count of times selected")
    # plt.title("Count of items selections, " + m)
    # plt.savefig(results_directory + 'item_plot_' + m + '_count.png', bbox_inches="tight")
    # plt.close(fig)

    # Plot percentages
    fig, ax = plt.subplots()
    count.plot(x='item', y='percent', kind='bar', figsize=(10, 6), rot=90, ax=ax, legend=False)
    plt.xlabel("Item")
    plt.ylabel("Percentage of sample who selected that item (%)")
    plt.title("Percentage of sample who selected each item, " + m)
    plt.savefig(results_directory + 'item_plot_' + m + '_percent.png', bbox_inches="tight")
    plt.close(fig)

    plt.clf()

