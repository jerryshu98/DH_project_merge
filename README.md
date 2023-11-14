# Data Loader and Viewer

This repository contains two Python scripts, `data_loader.py` and `data_viewer.py`, designed for handling and visualizing data from different tables.

## data_loader.py

### Overview

The `data_loader.py` script is responsible for merging data from various tables and organizing it into a consolidated format. The final result is exported as `merged_data.csv`.

### Usage

1. Place your data files in the `data` directory.
2. Run the script using the following command:

    ```bash
    python data_loader.py
    ```

3. The script will process the data, merge tables, and output the consolidated data as `merged_data.csv` in the same directory.

## data_viewer.py

### Overview

The `data_viewer.py` script is designed to visualize specific data based on a given `stay_id`. It reads the `merged_data.csv` file and prints information related to the specified `stay_id`.

### Usage

1. After running `data_loader.py`, you will have a `merged_data.csv` file in the same directory.

2. Run the `data_viewer.py` script with the desired `stay_id` as a command-line argument. For example:

    ```bash
    python data_viewer.py 30005707
    ```

   Replace `30005707` with the specific `stay_id` you want to visualize.

3. The script will display information related to the provided `stay_id` from the merged data.


