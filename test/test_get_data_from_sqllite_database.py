import pe_exam_package as pe

def test_get_data_from_sqllite_database():
    str_sql_query = """ select * from qa_report """
    df_data = pe.get_data_from_sqllite_database(str_database_file_path = 'pe_exam/qa_report.db',
                                             str_sql_query = str_sql_query)
    
    assert df_data.empty == False