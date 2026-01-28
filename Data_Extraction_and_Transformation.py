import pandas as pd
import yaml
import os

root_folder = r'C:\Nithyanantham\Prepartion\Python_code_Linerar\data'
output_dir = "TickerFiles"

os.makedirs(output_dir, exist_ok=True)

all_rows = []

for month in os.listdir(root_folder):
    month_path = os.path.join(root_folder, month)

    if not os.path.isdir(month_path):
        continue

    for file_name in os.listdir(month_path):
        file_path = os.path.join(month_path, file_name)

        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)

            if not data:
                continue

            # YAML is a list of records
            if isinstance(data, list):
                for record in data:
                    all_rows.append(record)

            # If YAML is dict-based
            # elif isinstance(data, dict):
            #     for _, record in data.items():
            #         all_rows.append(record)

            else:
                print(f"Skipped unsupported format: {file_path}")

        except yaml.YAMLError as e:
            print(f" YAML parsing error in {file_path}: {e}")

        except Exception as e:
            print(f" Error processing file {file_path}: {e}")

# Create dataframe
try:
    df = pd.DataFrame(all_rows)
except Exception as e:
    raise RuntimeError(f"Failed to create DataFrame: {e}")

# Create one CSV per Ticker
try:
    for ticker, group in df.groupby('Ticker'):
        file_path = os.path.join(output_dir, f"{ticker}.csv")
        group.to_csv(file_path, index=False)
except KeyError:
    raise KeyError("Column 'Ticker' not found in data")
except Exception as e:
    raise RuntimeError(f"Error while writing ticker CSVs: {e}")

# Combine all ticker CSVs
try:
    market_df = pd.concat(
        [pd.read_csv(os.path.join(output_dir, f))
         for f in os.listdir(output_dir)],
        ignore_index=True
    )
except Exception as e:
    raise RuntimeError(f"Failed to combine CSV files: {e}")

# print("Data extraction and CSV generation completed successfully")
# print("Total tickers:", df['Ticker'].nunique())