"""Run project modules using a valid Python installation and installed dependencies."""
from pathlib import Path
import runpy
import sys

root = Path(__file__).resolve().parent
sys.path.insert(0, str(root))
sys.dont_write_bytecode = True
module = sys.argv.pop(1)
if module == 'tests':
    import importlib
    import inspect
    import unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for path in sorted((root / 'tests').rglob('*.py')):
        if '__pycache__' in path.parts or path.name == '__init__.py':
            continue
        name = 'tests.' + '.'.join(path.relative_to(root / 'tests').with_suffix('').parts)
        test_module = importlib.import_module(name)
        suite.addTests(loader.loadTestsFromModule(test_module))
        for name, function in inspect.getmembers(test_module, inspect.isfunction):
            if name.startswith('test_') and function.__module__ == test_module.__name__:
                suite.addTest(unittest.FunctionTestCase(function))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
runpy.run_module(module, run_name='__main__')
