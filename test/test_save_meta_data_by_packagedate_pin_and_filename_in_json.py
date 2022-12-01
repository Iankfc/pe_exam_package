import pe_exam_package as pe
import os
import shutil


def test_save_meta_data_by_packagedate_pin_and_filename_in_json():
    
    if os.path.exists('output'):
        shutil.rmtree('output')
    
    df_input_data = pe.get_data_from_input_file_csv(str_input_data_csv_file_path = r"pe_exam/input_file.csv")
    pe.save_meta_data_by_packagedate_pin_and_filename_in_json(df_input_data = df_input_data,
                                                            str_database_file_path = 'pe_exam/qa_report.db')
    assert os.path.exists('output')