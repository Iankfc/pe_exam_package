import pe_exam_package as pe
import json
import os


def save_meta_data_by_packagedate_pin_and_filename_in_json(df_input_data = None,
                                                           str_database_file_path = None):
    """ This function allows you to save the meta data by package date pin and filename in JSON format.

    Args:
        df_input_data (pandas dataframe, required): Directory name found in the 'input_file.csv'. Defaults to None.
        str_database_file_path (str, required): File path where the SQLLite database is saved. Defaults to None.

    Returns:
        Multiple JSON files inside the output folder
    """
        
    for int_row_index in range(df_input_data.shape[0]): # 
        str_pin = df_input_data['pin'][int_row_index] # Get PIN
        str_date = df_input_data['directory_name'][int_row_index].split('_')[5].split('-')[0] # Get date by splitting directory name by '_' and then by '-' then get the first element
        str_date = str_date[0:4] + '-' + str_date[4:6] + '-' + str_date[6:8] # Format date
        str_directory_name = df_input_data['directory_name'][int_row_index] # Get directory name
        
        list_json_data = pe.get_meta_data_list_json_by_directory(str_directory_name = str_directory_name,
                                                                str_database_file_path = str_database_file_path) # Get meta data list in JSON format by directory name
        
        for dict_json_meta_data in list_json_data: # Loop through each JSON meta data
            str_meta_data_filename = dict_json_meta_data['audio_file_name'].replace('.wav','_meta.json') # Replace '.wav' with '_meta.json'
            
            str_output_folder_path = f'output/{str_date}/{str_pin}' # Output folder path
            
            if not os.path.exists(str_output_folder_path): # If output folder path does not exist
                os.makedirs(str_output_folder_path) # Create output folder path
            
            str_output_file_path = f'{str_output_folder_path}/{str_meta_data_filename}' # Output file path
            with open(str_output_file_path, 'w') as obj_json_file: # Open JSON file
                json.dump(dict_json_meta_data, obj_json_file) # Save JSON file
                
            pass
        
if __name__ == '__main__':
    df_input_data = pe.get_data_from_input_file_csv(str_input_data_csv_file_path = r"pe_exam/input_file.csv")
    save_meta_data_by_packagedate_pin_and_filename_in_json(df_input_data = df_input_data,
                                                           str_database_file_path = 'pe_exam/qa_report.db')