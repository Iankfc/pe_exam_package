__version__ = '0.1.0'

try:
    from pe_exam_package.api.get_data_from_sqllite_database import get_data_from_sqllite_database
except ImportError:
    print('ImportError')
    pass