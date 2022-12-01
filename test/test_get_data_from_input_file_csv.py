import pe_exam_package as pe


def test_get_data_from_input_file_csv():
    df_data = pe.get_data_from_input_file_csv(str_input_data_csv_file_path = r"pe_exam/input_file.csv")
    assert df_data.empty == False