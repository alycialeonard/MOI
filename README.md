# Markers of Inequality Study

*Paper preprint*:

This repo contains the code for UK PACT "Markers of Inequality" study on intersectionality in needs assessment for development planning.

This method was developed using a [case study dataset collected in Siaya County, Kenya](https://doi.org/10.5281/zenodo.7835350).
This dataset covers, amongst other things, data on which items people prioritize most in their daily lives and the reasons why (i.e., their values).
[More information on the case study dataset is available here](https://doi.org/10.2139/ssrn.4496252).

### How to run the analysis

To run the analysis, first ensure that `Siaya_UPV_survey.csv` and `Siaya_UPV_Utterances.csv` are in the `\data` folder. 
These can be retrieved from the dataset link if needed.
Then, run the data pre-processing by issuing the following command from the `MOI` directory:

`python preprocess_data.py`

This will generate two new files, `Siaya_UPV_survey_Prepared.csv` and `Siaya_UPV_Utterances_Prepared.csv`.
These files contain one-hot columns for each demographic marker to evaluate. 
Now, you can run any of the analysis scipts from the `MOI` directory using a command structured as:

`python <script_name_here>.py`

### About the analysis scripts

Each script does a different type of analysis. There are generally three types:
1. Map the intersectionality of the sample (i.e., `intersectionality.py`)
2. Map the prioritization of items across demographics (i.e., `item_<x>.py`)
3. Map the weight placed on values across demographics (i.e., `value_<x>.py`)

The `<x>` above can contain a number of either-or flags about the type of analysis in the script. These are:
- `matrix` vs `plots`: The scripts which include "matrix" in the filename produce heatmap matrices, while those which include "plots" create bar charts.
- `intersections` vs `singlemarker`: The scripts which include "intersections" analyse each intersection of two demographics, while those which include "singlemarker" analyse each individual demographic.
- `counts` vs `weighted`: The value scripts which end with "counts" analyse the frequency of each value relative to all values annotated across each group.
However, as values were elicited with why-probing in which different people may speak different amounts, this can literally under-value less talkative community members.
The scripts which end with "weighted" address this by instead calculating a weighted sum of value annotations.
Each respondent is assigned a value weight of 1, distributed proportionally across the values they mentioned. 

With these flags in mind, a quick summary of the purpose of each script is listed below. Details about each analysis are summarized in the header of each script.

- `intersectionality`: Generate a matrix of the intersectionality of the dataset sample.
- `item_matrix_intersections`: Generate matrices showing how each demographic intersection prioritizes each item.
- `item_matrix_singlemarkers`: Generate matrices showing how each individual demographic prioritizes each item. 
- `item_plots`: Generate bar charts of ranked item prioritisation for each individual demographic.
- `value_matrix_intersections_counts`: Generate matrices showing how frequently each demographic intersection referred to each value (percentage).
- `value_matrix_intersections_weighted`: Generate matrices showing how frequently each demographic intersection referred to each value (weighted sum).
- `value_matrix_singlemarkers_counts`: Generate matrices showing how frequently each individual demographic referred to each value (percentage).
- `value_matrix_singlemarkers_weighted`: Generate matrices showing how frequently each individual demographic referred to each value (weighted sum).
- `value_plots_counts`: Generate bar charts of ranked value frequency for each individual demographic (percentage).
- `value_plots_weighted`: Generate bar charts of ranked value frequency for each individual demographic (weighted sum).

### How to customize the analysis

While these scripts are tailored to the sample dataset, they can be modified for any dataset including demographics which can be one-hot encoded and needs-related data.
This can be done by editing the pre-processing file to create one-hot columns for demographics of interest, and replacing the item/value lists/references with the relevant needs-assessment datapoint in your own dataset throughout the code. 