# **pe_exam_package**

## Table of Contents

- [About](#about)
- [Instruction](#Instruction)


## **About** <a name = "about"></a>

**pe_exam_package** is a python program that formats the data into JSON format between call extract and metadata.

## **Instruction** <a name = "Instruction"></a>

<br>

1. Using the windows CMD Terminal, create a new python environment with python version 3.9.5 installed.

```cmd

conda create --name pe_exam_package_environment python=3.9.5

```
2. Next, activate the virtual environment that you just created now. In the windows terminal, type the following commands.


```cmd

conda activate pe_exam_package_environment

```

3. Pip install the package from github


```cmd

pip3 install git+https://github.com/Iankfc/pe_exam_package.git@master

```

4. Finally, supply the required input parameters and use the sample code below to generate the output. 


```python

import pe_exam_package as pe

pe.get_metadata_and_tx_data_in_json_format(str_input_data_csv_file_path = r"pe_exam/input_file.csv",
                                            str_database_file_path = 'pe_exam/qa_report.db',
                                            str_extract_txt_file_path = 'pe_exam/extract.txt')

```


## **Parameters**

Name | Type | Description | Example
------ | ------ |------ |------ 
**str_input_data_csv_file_path** | str | A CSV file containing the list of directory name needed to generate the output which contains the directory_name and pin | 'pe_exam/input_file.csv'
**str_database_file_path** | str | A SQLLite database containing the following information: <br> directory_name, corpus_code, file_path, audio_duration, email, user_id, gender, native_language  | 'pe_exam/qa_report.db'
**str_extract_txt_file_path** | str | A text file containing several utterances | 'pe_exam/extract.txt'




[[Back to top]](#)  