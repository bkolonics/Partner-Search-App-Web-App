import sqlite3 as sq
import pandas as pd

def excel_to_dataframe(file: str, **kwargs: str) -> pd.DataFrame:
    """Converts excel file to dataframe"""
    return pd.read_excel(file, **kwargs)

def dataframe_to_sql(file: str, table: str, **kwargs: str):
    conn = sq.connect('ecsel_database.db')
    return file.to_sql(table, conn, if_exists='replace')
 
if __name__ == '__main__':
    
    dataframe_to_sql(excel_to_dataframe('assets/projects.xlsx',
                    sheet_name='Sheet1'), 'pojects')
    dataframe_to_sql(excel_to_dataframe('assets/participants.xlsx',
                    sheet_name='Sheet1'), 'participants')
    dataframe_to_sql(excel_to_dataframe('assets/countries.xlsx',
                    sheet_name='Countries'), 'countries')