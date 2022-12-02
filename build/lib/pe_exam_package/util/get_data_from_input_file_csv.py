import pandas as pd

def get_data_from_input_file_csv(str_input_data_csv_file_path = None):
    """This function allows you to read data from a csv file and dowload the data in pandas dataframe format.

    Args:
        str_input_data_csv_file_path (str, required): File path of the CSV file. Defaults to None.

    Returns:
        pandas dataframe
    """
    
    df_data = pd.read_csv(str_input_data_csv_file_path) # Read data from CSV file
    
    return df_data

if __name__ == "__main__":
    df_data = get_data_from_input_file_csv(str_input_data_csv_file_path = "pe_exam/input_file.csv")
    pass