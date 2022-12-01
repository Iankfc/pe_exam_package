import pandas as pd

def get_data_from_input_file_csv(str_input_data_csv_file_path = None):
    
    df_data = pd.read_csv(str_input_data_csv_file_path)
    
    return df_data

if __name__ == "__main__":
    df_data = get_data_from_input_file_csv(str_input_data_csv_file_path = r"pe_exam/input_file.csv")
    pass