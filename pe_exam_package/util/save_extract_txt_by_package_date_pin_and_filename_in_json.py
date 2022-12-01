import pe_exam_package as pe
import json
import os
import pandas as pd

def save_extract_txt_by_package_date_pin_and_filename_in_json(df_input_data = None,
                                                              str_directory_name = None,
                                                              str_database_file_path = None,
                                                              str_extract_txt_file_path = None):
    
    for int_row_index in range(df_input_data.shape[0]):
        str_pin = df_input_data['pin'][int_row_index]
        str_date = df_input_data['directory_name'][int_row_index].split('_')[5].split('-')[0]
        str_date = str_date[0:4] + '-' + str_date[4:6] + '-' + str_date[6:8]
        str_directory_name = df_input_data['directory_name'][int_row_index]
        
        str_sql_query = f""" select file_path from qa_report 
                            where directory_name = '{str_directory_name}'
                        """
        df_data = pe.get_data_from_sqllite_database(str_database_file_path = str_database_file_path,
                                                str_sql_query = str_sql_query)
    
        df_extract_txt = pe.get_extract_txt_in_dataframe_format(str_extract_txt_file_path = str_extract_txt_file_path)
        
        df_extract_txt = pd.merge(df_extract_txt,
                                  df_data,
                                  how = 'left',
                                  left_on = 'File',
                                  right_on = 'file_path')
        
        df_extract_txt = df_extract_txt[df_extract_txt['file_path'].notna()]
        
        
        for str_wav_file_path in df_extract_txt['File'].unique():
            
            df_output = df_extract_txt[df_extract_txt['File'] == str_wav_file_path]
            df_output = df_output[['speaker_tag','text','start','end']]
            list_json_output = json.loads(df_output.to_json(orient = 'records'))

            str_extract_data_filename = str_wav_file_path.replace('.wav','_tx.json')
            str_extract_data_filename = str_extract_data_filename.replace('/audio-efs/','')
            
            str_output_folder_path = f'output/{str_date}/{str_pin}'
            
            if not os.path.exists(str_output_folder_path):
                os.makedirs(str_output_folder_path)
            
            str_output_file_path = f'{str_output_folder_path}/{str_extract_data_filename}'
            with open(str_output_file_path, 'w') as obj_json_file:
                json.dump(list_json_output, obj_json_file)
                

    return None
    
if __name__ == '__main__':
    df_input_data = pe.get_data_from_input_file_csv(str_input_data_csv_file_path = r"pe_exam/input_file.csv")
    save_extract_txt_by_package_date_pin_and_filename_in_json(  df_input_data = df_input_data,
                                                                str_database_file_path = 'pe_exam/qa_report.db',
                                                                str_extract_txt_file_path = 'pe_exam/extract.txt')