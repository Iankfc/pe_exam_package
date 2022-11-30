#%%
import pandas as pd
import numpy as np

str_extract_txt_file_path = f'pe_exam/extract.txt'

#def convert_extract_from_txt_to_dataframe(str_extract_txt_file_path = None):

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

df_data_explode['TRANS'] = df_data_explode['TRANSCRIPTION'].str.split('<')

df_data_explode = df_data_explode.explode(['TRANS'])

df_data_explode = df_data_explode[df_data_explode['TRANS'] != ' ']
#%%
df_data_explode['TRANS'] = df_data_explode['TRANS'].apply(lambda x: '<' + x)

#%%

#df_data_explode = df_data_explode.drop_duplicates()
#pass
#return None


#%%

df_data_explode = df_data_explode[['INTERVAL','TRANS']]


#%%

df_data_explode['INTERVAL']  = df_data_explode['INTERVAL'].replace('\n','').str.strip()
#%%

df_data_explode['start'] = df_data_explode['INTERVAL'].str.split(' ', n = 2).str[0]

df_data_explode['end'] = df_data_explode['INTERVAL'].str.split(' ', n = 2).str[1]


df_data_explode = df_data_explode.reset_index()


#%%

df_data_explode['speaker_tag'] = df_data_explode['TRANS'].str.split('>', n = 1).str[0]

#%%

df_data_explode['speaker_tag'] = df_data_explode['speaker_tag'].apply(lambda x: str(x) + '>')


#%%

# df_data_explode['TRANS2'] = np.where(~df_data_explode['TRANS'].str.contains('spk'),
#                                      df_data_explode['TRANS'],
#                                      pd.NA)

#%%

# df_data_explode['TRANS2'] = df_data_explode['TRANS2'].fillna(method='bfill')
#%%

# if __name__ == '__main__':
#     convert_extract_from_txt_to_dataframe(str_extract_txt_file_path = f'pe_exam/extract.txt')
    
#%%