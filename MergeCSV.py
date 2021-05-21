# Run this to merge all the CSV files in the datasets folder into one
# Make sure to delete any older versions of the files

import os
import glob
import pandas as pd
os.chdir("datasets")


file_pattern = "csv"
list_of_files = [file for file in glob.glob('*.{}'.format(file_pattern))]
print(list_of_files)

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in list_of_files ])
#export to csv
combined_csv.to_csv( "data.csv", index=False, encoding='utf-8-sig')