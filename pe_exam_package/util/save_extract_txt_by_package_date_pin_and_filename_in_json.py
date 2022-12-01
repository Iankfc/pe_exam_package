import pe_exam_package as pe
import json
import os
import pandas as pd

def save_extract_txt_by_package_date_pin_and_filename_in_json(df_input_data = None,
                                                              str_directory_name = None,
                                                              str_database_file_path = None,
                                                              str_extract_txt_file_path = None):
    """ This function allows you to save the extract txt by package date pin and filename in JSON format.

    Args:
        df_input_data (pandas dataframe, required): Directory name found in the 'input_file.csv'. Defaults to None.
        str_directory_name (str, required): File path where the SQLLite database is saved. Defaults to None.
        str_database_file_path (str, required): File path where the SQLLite database is saved. Defaults to None.
        str_extract_txt_file_path (str, required): File path where the SQLLite database is saved. Defaults to None.

    Returns:
        Multiple JSON files inside the output folder
    """
    
    for int_row_index in range(df_input_data.shape[0]): # 
        str_pin = df_input_data['pin'][int_row_index] # Get PIN
        str_date = df_input_data['directory_name'][int_row_index].split('_')[5].split('-')[0] # Get date
        str_date = str_date[0:4] + '-' + str_date[4:6] + '-' + str_date[6:8] # Format date
        str_directory_name = df_input_data['directory_name'][int_row_index] # Get directory name
        
        str_sql_query = f""" select file_path from qa_report 
                            where directory_name = '{str_directory_name}'
                        """ # SQL query
        df_data = pe.get_data_from_sqllite_database(str_database_file_path = str_database_file_path,
                                                    str_sql_query = str_sql_query) # Get data from SQLLite database
    
        df_extract_txt = pe.get_extract_txt_in_dataframe_format(str_extract_txt_file_path = str_extract_txt_file_path) # Get extract txt in dataframe format
        
        df_extract_txt = pd.merge(df_extract_txt,
                                  df_data,
                                  how = 'left',
                                  left_on = 'File',
                                  right_on = 'file_path') # Merge extract txt and qa_report
        
        df_extract_txt = df_extract_txt[df_extract_txt['file_path'].notna()] # Filter extract txt by file path not null
        
        
        for str_wav_file_path in df_extract_txt['File'].unique(): # Loop through each wav file path
            
            df_output = df_extract_txt[df_extract_txt['File'] == str_wav_file_path] # Filter extract txt by wav file path
            df_output = df_output[['speaker_tag','text','start','end']] # Select columns
            list_json_output = json.loads(df_output.to_json(orient = 'records')) # Convert dataframe to JSON format

            str_extract_data_filename = str_wav_file_path.replace('.wav','_tx.json') # Get extract data filename and format it to replace .wav with _tx.json
            str_extract_data_filename = str_extract_data_filename.replace('/audio-efs/','') # Get extract data filename and format it to replace /audio-efs/ with nothing
            
            str_output_folder_path = f'output/{str_date}/{str_pin}' # Get output folder path
            
            if not os.path.exists(str_output_folder_path): # If output folder path does not exist
                os.makedirs(str_output_folder_path) # Create output folder path
            
            str_output_file_path = f'{str_output_folder_path}/{str_extract_data_filename}' # Get output file path
            with open(str_output_file_path, 'w') as obj_json_file: # Open output file path
                json.dump(list_json_output, obj_json_file) # Save JSON file
                

    return None
    
if __name__ == '__main__':
    df_input_data = pe.get_data_from_input_file_csv(str_input_data_csv_file_path = r"pe_exam/input_file.csv")
    save_extract_txt_by_package_date_pin_and_filename_in_json(  df_input_data = df_input_data,
                                                                str_database_file_path = 'pe_exam/qa_report.db',
                                                                str_extract_txt_file_path = 'pe_exam/extract.txt')