"""Real initialization, import safety, CLI, and bounded headless replay checks."""
import contextlib
import io
import os
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
import teoria_sistemas as model


ROOT = Path(__file__).resolve().parents[1]


def state(agents):
    return [(a.money, a.previous_money, a.is_employer, a.cooperation_index)
            for a in agents]


def legacy_initial_state(rng):
    result = []
    for _ in range(model.N):
        money = rng.randint(20, 100)
        employer = rng.choice([True, False])
        cooperation = rng.uniform(0.8, 1.2)
        result.append((money, money, employer, cooperation))
    return result


class InitializationTests(unittest.TestCase):
    def test_same_seed_repeats_full_state_and_creates_fresh_agents(self):
        first = model.initialize_agents(seed=42)
        second = model.initialize_agents(seed=42)
        self.assertEqual(state(first), state(second))
        self.assertEqual(len(first), 100)
        self.assertTrue(all(isinstance(a, model.Agent) for a in first))
        self.assertTrue(all(a is not b for a, b in zip(first, second)))

    def test_zero_negative_and_positive_seeds_match_legacy_draw_order(self):
        for seed in (0, -7, 42, 2026):
            with self.subTest(seed=seed):
                self.assertEqual(state(model.initialize_agents(seed=seed)),
                                 legacy_initial_state(random.Random(seed)))
        self.assertNotEqual(state(model.initialize_agents(seed=0)),
                            state(model.initialize_agents(seed=42)))

    def test_explicit_seed_does_not_touch_global_random_state(self):
        before = random.getstate()
        model.initialize_agents(seed=0)
        self.assertEqual(before, random.getstate())

    def test_omitted_seed_preserves_legacy_output_and_rng_progression(self):
        saved = random.getstate()
        self.addCleanup(random.setstate, saved)
        random.seed(2026)
        initial = random.getstate()
        expected = legacy_initial_state(random)
        expected_state = random.getstate()
        random.setstate(initial)
        self.assertEqual(state(model.initialize_agents()), expected)
        self.assertEqual(random.getstate(), expected_state)


class EntrypointTests(unittest.TestCase):
    def test_script_help_and_invalid_seed(self):
        for argv, status in [(['--help'], 0), (['--seed', 'oops'], 2)]:
            with self.subTest(argv=argv), tempfile.TemporaryDirectory() as directory:
                env = os.environ.copy()
                env.update(PYTHONDONTWRITEBYTECODE='1', MPLBACKEND='Agg',
                           MPLCONFIGDIR=directory)
                result = subprocess.run(
                    [sys.executable, str(ROOT / 'teoria_sistemas.py'), *argv],
                    cwd=directory, env=env, capture_output=True, text=True,
                    timeout=20)
                self.assertEqual(result.returncode, status, result.stderr)
                self.assertEqual(list(Path(directory).iterdir()), [])
                if status == 0:
                    self.assertIn('--seed', result.stdout)
                else:
                    self.assertIn('error:', result.stderr)

    def run_isolated(self, code):
        with tempfile.TemporaryDirectory() as directory:
            env = os.environ.copy()
            env.update(PYTHONPATH=str(ROOT), PYTHONDONTWRITEBYTECODE='1',
                       MPLBACKEND='Agg', MPLCONFIGDIR=directory)
            result = subprocess.run([sys.executable, '-c', code], cwd=directory,
                                    env=env, capture_output=True, text=True,
                                    timeout=20)
            self.assertEqual(list(Path(directory).iterdir()), [])
            self.assertEqual(result.returncode, 0, result.stderr)
            return result

    def test_import_is_nonexecuting_and_does_not_load_pyplot(self):
        result = self.run_isolated('''
import random
import sys
before = random.getstate()
import teoria_sistemas as model
assert random.getstate() == before
assert 'matplotlib.pyplot' not in sys.modules
assert not hasattr(model, 'agents')
assert not hasattr(model, 'total_satisfaction')
assert (model.N, model.T, model.initial_market_money) == (100, 500, 5000)
''')
        self.assertEqual(result.stdout, '')
        self.assertEqual(result.stderr, '')

    def test_help_and_invalid_seed_exit_before_initialization_and_plotting(self):
        for argv, status in [(['--help'], 0), (['--seed', 'oops'], 2),
                             (['--seed'], 2)]:
            with self.subTest(argv=argv):
                result = self.run_isolated('''
import sys
import teoria_sistemas as model
def forbidden(*args, **kwargs):
    raise AssertionError('initialization must not run')
model.initialize_agents = forbidden
try:
    model.main(%r)
except SystemExit as error:
    assert error.code == %r, error.code
else:
    raise AssertionError('expected SystemExit')
assert 'matplotlib.pyplot' not in sys.modules
''' % (argv, status))
                if status == 0:
                    self.assertIn('--seed', result.stdout)
                else:
                    self.assertIn('error:', result.stderr)


class NumericalReplayTests(unittest.TestCase):
    def test_actual_main_repeats_bounded_metrics_and_reports_seed_zero(self):
        import matplotlib
        matplotlib.use('Agg', force=True)
        import matplotlib.pyplot as plt
        self.addCleanup(plt.close, 'all')

        def run():
            output = io.StringIO()
            with mock.patch.object(model, 'T', 12), \
                    mock.patch.object(plt, 'show') as show, \
                    contextlib.redirect_stdout(output):
                model.main(['--seed', '0'])
                show.assert_called_once_with()
            self.assertEqual(output.getvalue(), 'Semilla: 0\n')
            lines = plt.gcf().axes[0].lines
            self.assertEqual(len(lines), 3)
            metrics = np.asarray([line.get_data_3d()[1] for line in lines])
            self.assertEqual(metrics.shape, (3, 12))
            self.assertTrue(np.isfinite(metrics).all())
            plt.close('all')
            return metrics

        before = random.getstate()
        np.testing.assert_array_equal(run(), run())
        self.assertEqual(before, random.getstate())


if __name__ == '__main__':
    unittest.main()
