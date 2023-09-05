'''
Analyses the percentage of all annotations which were each value for each individual demographic marker
Inputs: Prepared utterances data file, list of markers (i.e., one-hot columns in data file), list of values.
Outputs: Plots of value frequency, Excel file of values across dataset
Author: Alycia Leonard
Contact: alycia.leonard@eng.ox.ac.uk
Last edited: 2023-09-05
'''

import pandas as pd
import warnings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
warnings.simplefilter(action='ignore', category=FutureWarning)

# Define location of input data
utterances_filepath = "data\\Siaya_UPV_Utterances_Prepared.csv"
markers_filepath = 'parameters\\markers.csv'
values_filepath = 'parameters\\values.csv'

# Define path to save results
results_directory = "results\\"

# Load list of markers, list of values, utterances data
markers = pd.read_csv(markers_filepath).values.ravel().tolist()
values = pd.read_csv(values_filepath).values.ravel().tolist()
df = pd.read_csv(utterances_filepath,low_memory=False)

# For each marker
for m in markers:

    # Grab only the rows of the dataset with that vulnerability
    subset = df.loc[(df[m] == 1)]

    # Count the occurrence of values in each column (the annotations of extracts are split into up to 6 columns
    # as there can be multiple annotations per extract)
    counts_val1 = subset['Annotation 1'].value_counts()
    counts_val2 = subset['Annotation 2'].value_counts()
    counts_val3 = subset['Annotation 3'].value_counts()
    counts_val4 = subset['Annotation 4'].value_counts()
    counts_val5 = subset['Annotation 5'].value_counts()
    counts_val6 = subset['Annotation 6'].value_counts()
    counts_val7 = subset['Annotation 7'].value_counts()

    # Create dataframe to hold summed results
    count = pd.DataFrame(columns=['value', 'count'])

    # Concatenate frames for each column
    counts = pd.concat([counts_val1, counts_val2, counts_val3, counts_val4, counts_val5, counts_val6, counts_val7]).to_frame()
    # Make the index (value) a column
    counts['value'] = counts.index
    # Rename the first column as count
    counts.columns.values[0] = 'count'

    # Get the unique values
    values = counts['value'].unique()

    # Sum across values
    for v in values:
        s = counts.loc[counts['value'] == v, 'count'].sum()
        data = {"value": v, "count": s}
        count = count.append(data, ignore_index=True)

    # Sort values in descending order
    count = count.sort_values(by=['count'], ascending=False)

    # Normalize the values by dividing by the total number of value annotations.
    count['percent'] = (count['count'] / count['count'].sum())*100

    # Save the counts data to excel
    count.to_excel(results_directory + 'value_plot_' + m + '_percent.xlsx')

    # If there is some data to plot, plot counts and percentages
    if not count.empty:

        # # Plot counts
        # fig, ax = plt.subplots()
        # count.plot(x='value', y='count', kind='bar', figsize=(12, 6), rot=90, ax=ax, legend=False)
        # plt.xlabel("Value")
        # plt.ylabel("Count of times selected")
        # plt.title("Count of value annotations, " + m)
        # plt.savefig(results_directory + 'value_plot_' + m + '_count.png', bbox_inches="tight")
        # plt.close(fig)

        # Plot percentages
        fig, ax = plt.subplots()
        count.plot(x='value', y='percent', kind='bar', figsize=(12, 6), rot=90, ax=ax, legend=False)
        plt.xlabel("Value")
        plt.ylabel("Percentage of annotations which are this value (%)")
        plt.title("Percentage of annotations which are each value, " + m)
        plt.savefig(results_directory + 'value_plot_' + m + '_percent.png', bbox_inches="tight")
        plt.close(fig)

        plt.clf()

