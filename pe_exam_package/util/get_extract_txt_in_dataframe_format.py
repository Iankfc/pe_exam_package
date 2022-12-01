#%%
import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')


def get_extract_txt_in_dataframe_format(str_extract_txt_file_path = None):

    with open(str_extract_txt_file_path,'r') as file:
        list_extract_data = file.readlines()

    df_data = pd.DataFrame({'Header':list_extract_data})

    df_data['Value'] = df_data['Header'].str.split(':', n = 1).str[1]
    df_data['Header'] = df_data['Header'].str.split(':', n = 1).str[0]
    df_data['File'] = np.where( df_data['Header'] == 'FILE', df_data['Value'], np.nan)
    df_data['File'] = df_data['File'].fillna(method = 'ffill')
    df_data = df_data[df_data['Header'] != '\n']
    df_data_pivot = df_data.pivot_table(values='Value', index=['File'],
                        columns=['Header'], aggfunc=list)
    df_data_explode = df_data_pivot.explode(['TRANSCRIPTION','INTERVAL'])


    #%%

    df_data_explode = df_data_explode.reset_index()

    df_data_explode = df_data_explode[['File','INTERVAL','TRANSCRIPTION']]

    #%%

    df_data_explode['TRANS'] = df_data_explode['TRANSCRIPTION'].str.split('<#')

    #%%
    df_data_explode = df_data_explode.explode(['TRANS'])

    #%%

    del df_data_explode['TRANSCRIPTION']

    #%%


    df_data_explode = df_data_explode[df_data_explode['TRANS'] != ' ']
    #%%
    df_data_explode['TRANS'] = df_data_explode['TRANS'].apply(lambda x: '<#' + x if 'spk' in x  else x)
    df_data_explode['TRANS'] = df_data_explode['TRANS'].apply(lambda x: '<#' + x if  'no-speech' in x else x)


    #%%

    df_data_explode['Continuation'] = np.where((~df_data_explode['TRANS'].str.contains('#spk')) & (~df_data_explode['TRANS'].str.contains('no-speech')),
                                            df_data_explode['TRANS'],
                                            pd.NA)


    #%%

    df_data_explode['Continuation'] = df_data_explode['Continuation'].fillna(method = 'bfill')


    #%%


    df_data_explode['TRANS'] = np.where(df_data_explode['TRANS'].str.contains("~"),
                                        df_data_explode['TRANS'].str.replace ("~", '') + df_data_explode['Continuation'],
                                        df_data_explode['TRANS']
                                        )


    #%%

    df_data_explode = df_data_explode[df_data_explode['TRANS'].str.contains('<#')]


    #%%

    del df_data_explode['Continuation']


    #%%

    df_data_explode['INTERVAL']  = df_data_explode['INTERVAL'].replace('\n','').str.strip()
    #%%

    df_data_explode['start'] = df_data_explode['INTERVAL'].str.split(' ', n = 2).str[0]

    df_data_explode['end'] = df_data_explode['INTERVAL'].str.split(' ', n = 2).str[1]


    #%%

    del df_data_explode['INTERVAL']

    #%%

    df_data_explode['speaker_tag'] = df_data_explode['TRANS'].str.split('>', n = 1).str[0]

    #%%

    df_data_explode['speaker_tag'] = df_data_explode['speaker_tag'].apply(lambda x: str(x) + '>')


    #%%
    df_data_explode['text'] = df_data_explode['TRANS'].str.split('>', n = 1).str[1]

    # %%

    df_data_explode['text'] = np.where(df_data_explode['speaker_tag'].str.contains('<#no-speech>'),
                                    df_data_explode['speaker_tag'],
                                    df_data_explode['text'])

    #%%

    df_data_explode['speaker_tag'] = np.where(df_data_explode['speaker_tag'].str.contains('<#no-speech>'),
                                    "",
                                    df_data_explode['speaker_tag'])

    #%%

    df_output = df_data_explode[['File','speaker_tag','text','start','end']]


    #%%



    df_output['speaker_tag'] = df_output['speaker_tag'].str.replace('<#','')
    df_output['speaker_tag'] = df_output['speaker_tag'].str.replace('>','')

    #%%

    df_output['text'] = df_output['text'].str.replace('\n','')       
    df_output['text'] = df_output['text'].str.strip()
                                                    
    #%%

    return df_output

if __name__ == '__main__':

    df_output = get_extract_txt_in_dataframe_format(str_extract_txt_file_path = 'pe_exam/extract.txt')
        
    pass

