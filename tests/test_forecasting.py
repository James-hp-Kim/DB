from pathlib import Path
import csv,json,math,sys,tempfile,unittest,importlib.util
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'plugins/expert-hub/skills/expert'
sys.path.insert(0,str(SKILL/'scripts'))
import backtest as bt
class BacktestTests(unittest.TestCase):
    def setUp(self):
        self.path=SKILL/'examples'/'synthetic-monthly.csv'
        self.config=json.loads((SKILL/'examples'/'backtest-config.json').read_text())
        self.calendar,self.panel=bt.load_panel(self.path,'MS')
    def test_holdout_never_in_cv(self):
        folds,final=bt.make_folds(len(self.calendar),self.config)
        self.assertTrue(all(f['test_end']<=final['train_end'] for f in folds))
        self.assertEqual(final['test_end']-final['test_start'],self.config['horizon'])
    def test_future_change_does_not_change_selection(self):
        original=bt.baseline_selection(self.calendar,self.panel,self.config)
        altered={k:v[:-6]+[999999.0]*6 for k,v in self.panel.items()}
        changed=bt.baseline_selection(self.calendar,altered,self.config)
        self.assertEqual(original,changed)
    def test_gap_forecasts_without_gap_actual(self):
        self.config['gap']=2
        folds,final=bt.make_folds(len(self.calendar),self.config)
        rows=bt.evaluate(self.calendar,self.panel,[final],{'name':'naive'},self.config)
        self.assertEqual(min(r['lead'] for r in rows),3)
        changed={k:list(v) for k,v in self.panel.items()}
        for v in changed.values():v[final['train_end']:final['test_start']]=[1e9]*2
        altered=bt.evaluate(self.calendar,changed,[final],{'name':'naive'},self.config)
        self.assertEqual(rows,altered)
    def test_rolling_window(self):
        self.config['train_window']=36
        folds,final=bt.make_folds(120,self.config)
        self.assertTrue(all(f['train_end']-f['train_start']==36 for f in folds+[final]))
    def test_metrics_zero_denominator(self):
        rows=[dict(actual=0.,prediction=2.,mase_scale=0.,unique_id='a',origin='x',ds='z')]
        m=bt.score_rows(rows)
        self.assertIsNone(m['wape']);self.assertIsNone(m['mase']);self.assertEqual(m['mase_defined_n'],0)
        self.assertEqual(m['mae'],2);self.assertEqual(m['bias'],2)
    def test_negative_revenue_definition(self):
        rows=[dict(actual=-10.,prediction=-8.,mase_scale=2.,unique_id='a',origin='x',ds='z')]
        m=bt.score_rows(rows);self.assertEqual(m['wape'],20);self.assertEqual(m['mase'],1)
    def test_seasonal_long_horizon(self):
        self.assertEqual(bt.predict([1,2,3,4],6,{'name':'seasonal_naive','season_length':4}),[1,2,3,4,1,2])
    def test_reference_series_ids(self):
        self.assertIn('001',self.panel)
    def test_duplicate_missing_nan_calendar(self):
        cases=[
            'unique_id,ds,y\na,2020-01-01,1\na,2020-01-01,2\n',
            'unique_id,ds,y\na,2020-01-01,1\na,2020-03-01,2\n',
            'unique_id,ds,y\na,2020-01-01,nan\n',
            'unique_id,ds,y\na,2020-01-01,1\nb,2020-02-01,2\n',
            'unique_id,ds,y\na,2020-01-01,\n']
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'input.csv'
            for content in cases:
                p.write_text(content)
                with self.assertRaises(ValueError):bt.load_panel(p,'MS')
    def test_too_short_rejected(self):
        with self.assertRaises(ValueError):bt.validate_config(self.config,30)
    def test_same_predictions_scored_for_all_baselines(self):
        selected,ranking,rows=bt.baseline_selection(self.calendar,self.panel,self.config)
        models={r['model'] for r in rows}
        keys=[{(r['unique_id'],r['origin'],r['lead']) for r in rows if r['model']==m} for m in models]
        self.assertTrue(all(k==keys[0] for k in keys));self.assertEqual(len(keys[0]),72)
    def test_overlap_counts(self):
        self.config['step']=1
        rows=bt.evaluate(self.calendar,self.panel,bt.make_folds(120,self.config)[0],{'name':'naive'},self.config)
        m=bt.score_rows(rows);self.assertLess(m['unique_targets'],m['n'])
    @unittest.skipUnless(importlib.util.find_spec('sklearn'),'Optional ML runtime not installed')
    def test_ridge_recursive_and_finite(self):
        result=bt.predict(self.panel['001'][:70],12,{'name':'ridge','lags':12,'alpha':1.})
        self.assertEqual(len(result),12);self.assertTrue(all(math.isfinite(v) for v in result))


