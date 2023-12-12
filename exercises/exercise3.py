import pandas as pd
import sqlite3

use_cols = [0,1,2,12,22,32,42,52,62,72]

def download_from_url(url):
    data = pd.read_csv(url, low_memory=False, sep=';',encoding='latin-1', dtype = {1: str}, skiprows = 6, usecols = use_cols)
    data = data[:-4]

    column_names = ['date', 'CIN', 'name', 'petrol', 'diesel', 'gas', 'electro', 'hybrid', 'plugInHybrid', 'others']
    data.columns = column_names

    # remove columns with invalid CIN values
    data = data[data['CIN'].str.len() == 5]

    # remove rows with non-positive values
    postive_columns = ['petrol', 'diesel', 'gas', 'electro', 'hybrid', 'plugInHybrid', 'others']

    for column in postive_columns:
        data = data[data[column] != '-']

    data[postive_columns] = data[postive_columns].astype(int)

    for column in postive_columns:
        data = data[data[column] > 0]
    return data

def save_to_sql(data):
    conn = sqlite3.connect("cars.sqlite")
    cursor = conn.cursor()
    create_table_query = f"CREATE TABLE IF NOT EXISTS cars ({', '.join([f'{col} {data[col].dtype}' for col in data.columns])});"
    cursor.execute(create_table_query)
    data.to_sql("cars", conn, if_exists="replace", index=False)
    conn.close()

if __name__=="__main__":
    url = "https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0021_00.csv"
    data = download_from_url(url)
    save_to_sql(data)