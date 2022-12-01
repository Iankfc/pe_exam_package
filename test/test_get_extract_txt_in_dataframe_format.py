import pe_exam_package as pe

def test_get_extract_txt_in_dataframe_format():
    df_output = pe.get_extract_txt_in_dataframe_format(str_extract_txt_file_path = 'pe_exam/extract.txt')
    assert df_output.empty == False
    assert list(df_output.columns) == ['File', 'speaker_tag', 'text', 'start', 'end']