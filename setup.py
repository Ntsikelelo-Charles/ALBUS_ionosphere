# setup.py
# a setup file to help compile a C/C++ code module for Python
# 2006 ??? ??  James M Anderson  --JIVE  start
# 2007 Jan 10  JMA  --revise to also use Numarray stuff
# 2016 April AGW - changed for numpy and got rid of all numarray-related stuff
# 2019 July  AGW - script should now handle python 2 or python 3 

from setuptools import setup, Extension
from platform import python_version
import sys
import numpy

maj_ver = "1"
min_ver = "0"
ALBUS_PATH = "/optsoft/ALBUS"
# include_src="source_dir/include"
include_src=ALBUS_PATH+"/include"
# You can pass ALBUS_PATH this way or let your CMakeLists.txt detect it from the env

module1 = Extension('AlbusIonosphere',
                    define_macros = [('MAJOR_VERSION', maj_ver),
                                     ('MINOR_VERSION', min_ver)],
                    libraries = ['mim',
                                 'jmavex',
                                 'iri',
                                 'pim',
                                 'sofa',
                                 'vexplus',
                                 'vex',
                                 'fl',
                                 'gfortran',
#                                'lapacke',
                                 'm'],
                    library_dirs = [ALBUS_PATH+'/lib'],
                    runtime_library_dirs = [ALBUS_PATH+'/lib'],
                    include_dirs = [numpy.get_include(),include_src],
                    sources = ['AlbusIonosphere.cxx'])

setup (name = 'AlbusIonosphere',
       version = maj_ver+'.'+min_ver,
       description = 'ALBUS Ionospheric Calibration package for AIPS',
       long_description = '''
ALBUS Ionospheric Calibration package for AIPS
Currently in a development stage.
''',
       ext_modules = [module1])
