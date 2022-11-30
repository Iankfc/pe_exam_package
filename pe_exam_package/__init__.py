__version__ = '0.2.0'

try:
    from pe_exam_package.api.get_data_from_sqllite_database import get_data_from_sqllite_database
    from pe_exam_package.util.get_meta_data_list_json_by_directory import get_meta_data_list_json_by_directory
except ImportError:
    print('ImportError')
    pass