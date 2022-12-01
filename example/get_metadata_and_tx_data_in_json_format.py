import pe_exam_package as pe

pe.get_metadata_and_tx_data_in_json_format(str_input_data_csv_file_path = r"pe_exam/input_file.csv",
                                            str_database_file_path = 'pe_exam/qa_report.db',
                                            str_extract_txt_file_path = 'pe_exam/extract.txt')
    