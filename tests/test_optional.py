"""Optional integration checks: run with openpyxl and PyOD installed."""
import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'plugins/expert-hub/skills/expert/scripts'))
from analysis import anomalies
from convert_xlsx import convert
from openpyxl import Workbook


class OptionalTests(unittest.TestCase):
    def test_multivariate_known_extreme(self):
        result = anomalies(ROOT/'examples/deep-features.csv', values=['thickness','pressure','temperature'], top=5)
        self.assertEqual(result['findings'][0]['record'], 100)
        self.assertEqual(len(result['findings']), 5)
        self.assertTrue(all(f['type'] == 'review_priority_only' for f in result['findings']))
        repeated = anomalies(ROOT/'examples/deep-features.csv', values=['thickness','pressure','temperature'], top=5)
        self.assertEqual(result, repeated)

    def test_excel_row_trace_and_hidden_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, out = Path(tmp)/'원본.xlsx', Path(tmp)/'output.csv'
            book = Workbook()
            sheet = book.active
            sheet.title = '검사'
            sheet.append(['lot','inspected','defective'])
            sheet.append(['A',100,2])
            sheet.append(['B',50,0])
            sheet.row_dimensions[3].hidden = True
            book.save(source)
            book.close()
            result = convert(source, '검사', out)
            self.assertEqual(result['rows'],2)
            with out.open(encoding='utf-8-sig', newline='') as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual([r['__source_excel_row'] for r in rows], ['2','3'])
            with self.assertRaises(FileExistsError):
                convert(source,'검사',out)

    def test_uncached_formula_rejected_without_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, out = Path(tmp)/'formula.xlsx', Path(tmp)/'output.csv'
            book = Workbook()
            sheet = book.active
            sheet.append(['value'])
            sheet.append(['=1+2'])
            book.save(source)
            book.close()
            with self.assertRaisesRegex(ValueError, 'Uncached formula'):
                convert(source, 'Sheet', out)
            self.assertFalse(out.exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
