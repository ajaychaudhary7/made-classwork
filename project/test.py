from sqlalchemy import create_engine, inspect
import os
import pandas as pd

from pipeline import (
    download_kaggle_competition_data,
    extract_zip,
    convert_to_db,
    reduce_mem_usage,
    load_and_transform,
    return_dtypes
)

def test_dataset_content(output_directory):
    z = 0
    files_to_check = ['test_sub.csv', 'train_sub.csv']
    for file_name in files_to_check:
        file_path = os.path.join(output_directory, file_name)
        if os.path.exists(file_path):
            print(f"{file_name} exists.")
        else:
            print(f"{file_name} does not exist. Extraction might not have been successful.")
            z = 1
    if z==0:
        print("Test Case Passed")

    else:
        print("Test Case Failed : File extraction failed")

def test_dataset_transformation(output_directory):
    dtypes = return_dtypes()
    train_df = pd.read_csv(os.path.join(os.path.abspath(output_directory),'train_sub.csv'),low_memory=False)
    train_df, good_cols = load_and_transform(train_df,train=True)

    test_dtypes = {k: v for k, v in dtypes.items() if k in good_cols}
    test_df = pd.read_csv(os.path.join(os.path.abspath(output_directory),'test_sub.csv'),usecols=good_cols[:-1],low_memory=False)
    test_df = load_and_transform(test_df,train=False)
    min_rows_required = 50000
    if len(train_df) >= min_rows_required and len(test_df) >= min_rows_required:
        print(f"Dataset Transformation: Test Passed. Both train.csv and test.csv have at least {min_rows_required} rows.")
    else:
        print(f"Dataset Transformation: Test Failed. Insufficient rows in train.csv or test.csv.")
    print("Dataset Transformation: Test Passed")

def check_table_existence(output_directory, table_name):
    db_path = os.path.join(output_directory, f"{table_name}.sqlite")
    engine = create_engine(f"sqlite:///{db_path}")
    
    inspector = inspect(engine)
    # Check if a table exists in the database
    exists = inspector.has_table(table_name)
    assert exists, f"The table '{table_name}' does not exist in the database."

def test_dataset_loader(output_directory):
    check_table_existence(output_directory, 'train')
    print("test_dataset_loader: 'train' Table exists, Test Passed")

    check_table_existence(output_directory, 'test')
    print("test_dataset_loader: 'test' Table exists, Test Passed")



def test_pipeline():
    kaggle_competition_name = "microsoft-malware-prediction"
    output_directory = "../data/"

    test_dataset_content(output_directory)
    test_dataset_transformation(output_directory)
    test_dataset_loader(output_directory)

if __name__ == "__main__":
    test_pipeline()