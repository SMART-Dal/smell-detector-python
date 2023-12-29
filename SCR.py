import pprint
from zipfile import ZipFile

path = 'dist/PySmellDetector-1.0.0-py3-none-any.whl'
names = ZipFile(path).namelist()
pprint.pprint(names)
