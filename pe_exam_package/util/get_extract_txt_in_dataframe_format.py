#%%
import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')
import datetime

def get_milliseconds_from_text_time(str_time = None):

    h,m,s = str_time.split(':')
    return int(float(datetime.timedelta(hours=int(h),minutes=int(m),seconds=float(s)).total_seconds())*1000)

def get_extract_txt_in_dataframe_format(str_extract_txt_file_path = None):
    """ This function allows you extract the text file containing the conversation and outputs a formatted dataframe version of the text file.

    Args:
        str_extract_txt_file_path (str, required): File path of the extract.txt file. Defaults to None.

    Returns:
        Pandas dataframe
    """

    with open(str_extract_txt_file_path,'r') as file: # Open the extract.txt file
        list_extract_data = file.readlines() # Read the extract.txt file

    df_data = pd.DataFrame({'Header':list_extract_data}) # Convert the extract.txt file to a dataframe

    df_data['Value'] = df_data['Header'].str.split(':', n = 1).str[1] # Split the dataframe into two columns and extract the value in the second column
    df_data['Header'] = df_data['Header'].str.split(':', n = 1).str[0] # Split the dataframe into two columns and extract the header in the first column
    df_data['File'] = np.where( df_data['Header'] == 'FILE', df_data['Value'], np.nan)  # Create a new column called 'File' and populate it with the value in the 'Value' column if the 'Header' column is 'FILE'
    df_data['File'] = df_data['File'].fillna(method = 'ffill') # Forward fill the 'File' column
    df_data = df_data[df_data['Header'] != '\n'] # Remove rows where the 'Header' column is a new line
    df_data_pivot = df_data.pivot_table(values='Value', index=['File'], 
                                        columns=['Header'], aggfunc=list) # Pivot the dataframe
    df_data_explode = df_data_pivot.explode(['TRANSCRIPTION','INTERVAL']) # Explode the dataframe


    #%%

    df_data_explode = df_data_explode.reset_index() # Reset the index

    df_data_explode = df_data_explode[['File','INTERVAL','TRANSCRIPTION']] # Select the columns we want

    #%%

    df_data_explode['TRANS'] = df_data_explode['TRANSCRIPTION'].str.split('<#') # Split the 'TRANSCRIPTION' column into two columns using '<#' as the delimiter

    #%%
    df_data_explode = df_data_explode.explode(['TRANS']) # Explode the dataframe

    #%%

    del df_data_explode['TRANSCRIPTION'] # Delete the 'TRANSCRIPTION' column
    
    #%%


    df_data_explode = df_data_explode[df_data_explode['TRANS'] != ' '] # Remove rows where the column TRAN is a space
    
    #%%
    df_data_explode['TRANS'] = df_data_explode['TRANS'].apply(lambda x: '<#' + x if 'spk' in x  else x) # Add '<#' to the start of the string if 'spk' is in the string
    df_data_explode['TRANS'] = df_data_explode['TRANS'].apply(lambda x: '<#' + x if  'no-speech' in x else x) # Add '<#' to the start of the string if 'no-speech' is in the string


    #%%

    df_data_explode['Continuation'] = np.where((~df_data_explode['TRANS'].str.contains('#spk')) & (~df_data_explode['TRANS'].str.contains('no-speech')),
                                                df_data_explode['TRANS'],
                                                pd.NA) # Create a new column called 'Continuation' and populate it with the value in column TRAN if the string does not contain '#spk' or 'no-speech'


    #%%

    df_data_explode['Continuation'] = df_data_explode['Continuation'].fillna(method = 'bfill') # Back fill the 'Continuation' column


    #%%


    df_data_explode['TRANS'] = np.where(df_data_explode['TRANS'].str.contains("~"),
                                        df_data_explode['TRANS'].str.replace ("~", '') + df_data_explode['Continuation'],
                                        df_data_explode['TRANS']
                                        ) # Replace '~' with '' and concatenate the 'Continuation' column IF the string contains '~'


    #%%

    df_data_explode = df_data_explode[df_data_explode['TRANS'].str.contains('<#')] # Remove rows where the column TRAN does not contain '<#'


    #%%

    del df_data_explode['Continuation'] # Delete the 'Continuation' column


    #%%

    df_data_explode['INTERVAL']  = df_data_explode['INTERVAL'].replace('\n','').str.strip() # Remove the new line character and strip the white space from the 'INTERVAL' column
    #%%

    df_data_explode['start'] = df_data_explode['INTERVAL'].str.split(' ', n = 2).str[0] # Split the 'INTERVAL' column into two columns and extract the start time in the first column

    df_data_explode['end'] = df_data_explode['INTERVAL'].str.split(' ', n = 2).str[1] # Split the 'INTERVAL' column into two columns and extract the end time in the second column


    #%%

    del df_data_explode['INTERVAL'] # Delete the 'INTERVAL' column

    #%%

    df_data_explode['speaker_tag'] = df_data_explode['TRANS'].str.split('>', n = 1).str[0] # Split the TRAN column into two columns and extract the speaker tag in the first column

    #%%

    df_data_explode['speaker_tag'] = df_data_explode['speaker_tag'].apply(lambda x: str(x) + '>') # Add '>' to the end of the string


    #%%
    df_data_explode['text'] = df_data_explode['TRANS'].str.split('>', n = 1).str[1] # Split the TRAN column into two columns and extract the text in the second column

    # %%

    df_data_explode['text'] = np.where(df_data_explode['speaker_tag'].str.contains('<#no-speech>'),
                                        df_data_explode['speaker_tag'],
                                        df_data_explode['text']) # Populate the 'text' column with the value in the 'speaker_tag' column if the 'speaker_tag' column contains '<#no-speech>'

    #%%

    df_data_explode['speaker_tag'] = np.where(df_data_explode['speaker_tag'].str.contains('<#no-speech>'),
                                                "",
                                                df_data_explode['speaker_tag']) # Populate the 'speaker_tag' column with '' if the 'speaker_tag' column contains '<#no-speech>'

    #%%

    df_output = df_data_explode[['File','speaker_tag','text','start','end']] # Select the columns we want


    #%%



    df_output['speaker_tag'] = df_output['speaker_tag'].str.replace('<#','') # Replace '<#' with ''
    df_output['speaker_tag'] = df_output['speaker_tag'].str.replace('>','') # Replace '>' with ''

    #%%

    df_output['text'] = df_output['text'].str.replace('\n','') # Replace the new line character with ''       
    df_output['text'] = df_output['text'].str.strip() # Strip the white space from the 'text' column
    
    df_output['File'] = df_output['File'].str.strip() # Strip the white space from the 'File' column
         
         
    df_output['text2'] = df_output['text'].str.split(']')
        
    df_output = df_output.explode('text2')        
    
    df_output = df_output.reset_index()
    df_output['AdditionalTimeStamp'] = np.nan
    
    for int_row_number in range(df_output.shape[0]):
        try:
            df_output['text'][int_row_number] = str(df_output['text2'][int_row_number]).split('[')[0]
            df_output['AdditionalTimeStamp'][int_row_number] = str(df_output['text2'][int_row_number]).split('[')[1]
        except IndexError:
            df_output['text'][int_row_number] =  df_output['text'][int_row_number] 
            df_output['AdditionalTimeStamp'][int_row_number] = np.nan
                              
    df_output['AdditionalTimeStamp']  = df_output['AdditionalTimeStamp'].astype(float)  * 1000            
    df_output['text'] = df_output['text'].str.strip()
    del df_output['text2']
    
    df_output = df_output[df_output['text'] != '']
    
    df_output['start2'] = df_output['start'].apply(lambda x: get_milliseconds_from_text_time(x))
    df_output['end2'] = df_output['end'].apply(lambda x: get_milliseconds_from_text_time(x))
    #%%

    return df_output

if __name__ == '__main__':

    df_output = get_extract_txt_in_dataframe_format(str_extract_txt_file_path = 'pe_exam/extract.txt')
        
    pass

