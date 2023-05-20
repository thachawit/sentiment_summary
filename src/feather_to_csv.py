import glob
import pandas as pd

# Get a list of file paths matching the Feather file pattern
feather_files = glob.glob('./Jan/*.feather')

# Loop through each Feather file
for feather_file in feather_files:
    # Read Feather file
    df = pd.read_feather(feather_file)

    # Get the base file name without extension
    file_name = feather_file.split('/')[-1].split('.')[0]

    # Convert to CSV and save
    csv_file = f'./Jan_csv/{file_name}.csv'
    df.to_csv(csv_file)
    # print(f'Converted {feather_file} to {csv_file}')
