import sqlite3
import pandas as pd

def get_data_from_sqllite_database(str_database_file_path = None,
                                   str_sql_query = None):
    """This function allows you to connect to a SQLLite database and dowload the data in pandas dataframe format.

    Args:
        str_database_file_path (str, required): The file path of you SQLLite database. Defaults to None.
        str_sql_query (str, required): SQL query. Defaults to None.

    Returns:
        Pandas Dataframe: data from SQLLite database in pandas dataframe format.
    """
    
    obj_db_connection = sqlite3.connect(fr'{str_database_file_path}')
    df_data = pd.read_sql(sql = str_sql_query, con = obj_db_connection)
    return df_data


if __name__ == '__main__':
    str_sql_query = """ select * from qa_report """
    df_data = get_data_from_sqllite_database(str_database_file_path = 'pe_exam/qa_report.db',
                                             str_sql_query = str_sql_query)
    pass
    