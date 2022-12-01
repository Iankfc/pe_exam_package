import pe_exam_package as pe

def get_metadata_and_tx_data_in_json_format(str_input_data_csv_file_path = None,
                                            str_database_file_path = None,
                                            str_extract_txt_file_path = None):
    """This function allows you to read data from a csv file and dowload the data in pandas dataframe format.

    Args:
        str_input_data_csv_file_path (str, required): File path of the CSV file containing the list of directory name needed to generate the output which contains the directory_name and pin. Defaults to None.
        
        str_database_file_path (str, required): File path of the SQLLite database containing the following information: <br> directory_name, corpus_code, file_path, audio_duration, email, user_id, gender, native_language. Defaults to None.
        
        str_extract_txt_file_path (str, required): File path containing the transcript of conversion and the timestamp. Defaults to None.
        
    Returns:
        Multiple JSON files inside the output folder
    """
    
    df_input_data = pe.get_data_from_input_file_csv(str_input_data_csv_file_path = str_input_data_csv_file_path) # Get data from input_file.csv
    
    pe.save_meta_data_by_packagedate_pin_and_filename_in_json(df_input_data = df_input_data,
                                                                str_database_file_path = str_database_file_path) # Save meta data by package date pin and filename in JSON format
    
    pe.save_extract_txt_by_package_date_pin_and_filename_in_json(  df_input_data = df_input_data,
                                                                str_database_file_path = str_database_file_path,
                                                                str_extract_txt_file_path = str_extract_txt_file_path) # Save extract txt by package date pin and filename in JSON format
    
    return None

if __name__ == '__main__':
    get_metadata_and_tx_data_in_json_format(str_input_data_csv_file_path = r"pe_exam/input_file.csv",
                                            str_database_file_path = 'pe_exam/qa_report.db',
                                            str_extract_txt_file_path = 'pe_exam/extract.txt')