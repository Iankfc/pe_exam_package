from setuptools import setup, find_packages
import pe_exam_package

classifiers = [
    'Developement Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9.5'
]

setup(
name = 'pe_exam_package',
version = pe_exam_package.__version__,
description = 'pe_exam_package is a python program that can take input and produce an output in json file',
url= 'https://github.com/Iankfc/pe_exam_package',
author='Christian Eslabon',
author_email='odesk5@outlook.com',
license = 'None',
classifiers=classifiers,
keywords='None',
packages=find_packages(),
use_scm_version=True,
include_package_data=True,
setup_requires=['setuptools_scm'],
install_requires = open('requirements.txt','r').read().split('\n')
)