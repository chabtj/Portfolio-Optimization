#script to combine all the csv files of a folder and then filter our comapny from the dataset i.e. BPCL 
import os
import glob
import pandas as pd
os.chdir("/Users/tejasvichabbra/Desktop/Portfolio_Analysis/csv_data")##give path to all csv's
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.loc[:,['SYMBOL','SERIES','CLOSE','TIMESTAMP']].to_csv( "/Users/tejasvichabbra/Desktop/Portfolio_Analysis/combined.csv", index=False, encoding='utf-8-sig')
