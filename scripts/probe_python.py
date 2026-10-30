import importlib.util
import json
import sqlite3
import sys

if sys.version_info < (3, 11):
    raise SystemExit('Python 3.11+ is required')
connection = sqlite3.connect(':memory:')
connection.execute('CREATE VIRTUAL TABLE check_fts USING fts5(x)')
connection.close()
if '--packages' in sys.argv:
    print(json.dumps({name: importlib.util.find_spec(name) is not None for name in ('openpyxl','pyod','scipy','statsmodels')}))
else:
    print(sys.executable)
