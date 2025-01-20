# Markers of Inequality (MOI): Intersectional Needs Assessment

This repo contains code to study intersectionality in needs assessment for development planning.
It accompanies the paper "[Shedding light on vulnerability: Intersectional energy planning for development](https://doi.org/10.1016/j.rser.2024.115199)".

This method was developed using a [case study dataset collected in Siaya County, Kenya](https://doi.org/10.5281/zenodo.7835350).
This dataset covers, amongst other things, data on which items people prioritize most in their daily lives and the reasons why (i.e., their values).
[More information on the case study dataset is available here](https://doi.org/10.1016/j.dib.2024.110317).

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

Each script does a different type of analysis. There are generally two types:
1. Map the intersectionality of the sample (i.e., `intersectionality.py`)
2. Map the prioritization of items across demographics (i.e., `item_matrix_<x>.py`)

The `<x>` contains flags about the type of analysis in the script. These are:
- `intersections` vs `singlemarker`: The scripts which include "intersections" analyse each intersection of two demographics, while those which include "singlemarker" analyse each individual demographic.
- `climate` vs `general`: The scripts which include "climate" address the climate-event-specific needs, while the scripts which contain "general" address needs in daily life.

These scripts output both heatmap matrices and spreadsheets summarizing intersectional item prioritisation.

### How to customize the analysis

While these scripts are tailored to the sample dataset, they can be modified for any dataset including demographics which can be one-hot encoded and needs-related data.
This can be done by editing the pre-processing file to create one-hot columns for demographics of interest, and replacing the item/value lists/references with the relevant needs-assessment datapoint in your own dataset throughout the code. 

### Citation

If you make use of this codebase, please use the following citation: 

*Leonard, A., Nguti, K., Lanza, M. F., & Hirmer, S. (2025). 
Shedding light on vulnerability: Intersectional energy planning for development. 
Renewable and Sustainable Energy Reviews, 211, 115199. 
https://doi.org/10.1016/j.rser.2024.115199.*

```commandline
@article{leonard2025shedding,
  title={Shedding light on vulnerability: Intersectional energy planning for development},
  author={Leonard, Alycia and Nguti, Kuthea and Lanza, Micaela Flores and Hirmer, Stephanie},
  journal={Renewable and Sustainable Energy Reviews},
  volume={211},
  pages={115199},
  year={2025},
  publisher={Elsevier},
  doi={10.1016/j.rser.2024.115199}
}
```
