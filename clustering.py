from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd
import os

pd.set_option('display.max_columns', None)

# Get the current working directory, data directory, parameters directory
current_directory = os.getcwd()
data_directory = os.path.join(current_directory, "data")
demographic_data_filepath = os.path.join(data_directory, "Siaya_UPV_Survey_Prepared.csv")

# Define where to save results
results_savepath = os.path.join(current_directory, "results", "frequent_itemsets.xlsx")

# Load your demographic dataset
demographic_data = pd.read_csv(demographic_data_filepath)
# Find the index of the last non-NaN value in the ID column
last_non_nan_index = demographic_data["ID"].last_valid_index()
# Grab only the one-hot columns
demographic_data = demographic_data.loc[:, ["Youth", "Female", "Disabled", "Single", "Divorced", "Widowed",
                                            "No occupation", "Low social connectivity", "Low trust in others",
                                            "No social support groups", "No education", "Low education",
                                            "Low information access", "Low satisfaction with housing",
                                            "Previous flood or fire in home", "No mobile phone", "Low income",
                                            "Female-headed household",	"No electricity access",
                                            "Perceived difficulty accessing services"]]
# Make sure all columns are 0 or 1
demographic_data = demographic_data.replace(True, 1)
demographic_data = demographic_data.replace(False, 0)
demographic_data.fillna(0, inplace=True)
# Trim data to dataset length
df_trimmed = demographic_data.iloc[:last_non_nan_index + 1]

# Apply Apriori algorithm to find frequent itemsets
frequent_itemsets = apriori(df_trimmed, min_support=0.1, use_colnames=True)
frequent_itemsets.to_excel(results_savepath)
