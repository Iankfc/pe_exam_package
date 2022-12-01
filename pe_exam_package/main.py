import pe_exam_package as pe

def get_metadata_and_tx_data_in_json_format(str_input_data_csv_file_path = None,
                                            str_database_file_path = None,
                                            str_extract_txt_file_path = None):
    
    df_input_data = pe.get_data_from_input_file_csv(str_input_data_csv_file_path = str_input_data_csv_file_path)
    
    pe.save_meta_data_by_packagedate_pin_and_filename_in_json(df_input_data = df_input_data,
                                                                str_database_file_path = str_database_file_path)
    
    pe.save_extract_txt_by_package_date_pin_and_filename_in_json(  df_input_data = df_input_data,
                                                                str_database_file_path = str_database_file_path,
                                                                str_extract_txt_file_path = str_extract_txt_file_path)
    
    return None

if __name__ == '__main__':
    get_metadata_and_tx_data_in_json_format(str_input_data_csv_file_path = r"pe_exam/input_file.csv",
                                            str_database_file_path = 'pe_exam/qa_report.db',
                                            str_extract_txt_file_path = 'pe_exam/extract.txt')