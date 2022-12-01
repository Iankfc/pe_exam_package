
import pe_exam_package as pe
import pandas as pd
import json

def get_meta_data_list_json_by_directory(str_directory_name = None,
                                        str_database_file_path = None):
     """ This function allows you to get the meta data list in JSON format by directory name found in 'input_file.csv'.

     Args:
          str_directory_name (str, required): Directory name found in the 'input_file.csv'. Defaults to None.
          str_database_file_path (str, required): File path where the SQLLite database is saved. Defaults to None.

     Returns:
          Pandas dataframe
     """
     
     str_sql_query = f""" select * from qa_report 
                         where directory_name = '{str_directory_name}'
                    """ # SQL query
     df_data = pe.get_data_from_sqllite_database(str_database_file_path = str_database_file_path,
                                                  str_sql_query = str_sql_query) # Get data from SQLLite database

     df_data['audio_file_name'] =  df_data['file_path'].str.replace('/audio-efs/','') # Replace '/audio-efs/' with ''

     df_data['speaker_id'] = pd.NA # Create a new column 'speaker_id' and set it to NA

     for int_row_index in range(df_data.shape[0]): # Loop through each row
          str_email = df_data['email'][int_row_index] # Get email
          str_gender = df_data['gender'][int_row_index] # Get gender
          str_native_language = df_data['native_language'][int_row_index] # Get native language
          df_data['speaker_id'][int_row_index] = {"email":str_email,
                                                  "gender":str_gender,
                                                  "native_language":str_native_language} # Set speaker_id to a dictionary that contains email, gender and native_language

     df_data = df_data[['audio_file_name','audio_duration','corpus_code','speaker_id']] # Select columns

     list_json_data = json.loads(df_data.to_json(orient='records')) # Convert dataframe to JSON format

     return list_json_data

#%%

if __name__ == '__main__':
     list_json_data = get_meta_data_list_json_by_directory(str_directory_name = "Axel_04803_ENG_MUL_0002_20220605-192230" ,
                                                            str_database_file_path = 'pe_exam/qa_report.db')


     with open('text1.json', 'w') as obj_json_file:
          json.dump(list_json_data, obj_json_file)
     
     pass
