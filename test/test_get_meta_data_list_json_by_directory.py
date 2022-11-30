import pe_exam_package as pe

def test_get_meta_data_list_json_by_directory():
     list_json_data = pe.get_meta_data_list_json_by_directory(str_directory_name = "Axel_04803_ENG_MUL_0002_20220605-192230" ,
                                                             str_database_file_path = 'pe_exam/qa_report.db')
     assert list_json_data != []