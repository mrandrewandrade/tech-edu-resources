#!/usr/bin/env python3
"""Run the Commons source checks, retained tests and optional rendered-site audit."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def run(*command):
    print('+ ' + ' '.join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rendered', action='store_true')
    args = parser.parse_args()
    run(sys.executable, 'scripts/commons_glossary.py', 'validate')
    run(sys.executable, 'scripts/course_notes.py', 'validate')
    run(sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_*.py')
    for script in sorted((ROOT / 'site/assets').glob('*.js')):
        run('node', '--check', str(script))
    for pattern in ('test_*.js', 'test_*.mjs'):
        for test in sorted((ROOT / 'tests').glob(pattern)):
            run('node', str(test))
    if args.rendered:
        run(sys.executable, 'scripts/course_notes.py', 'validate-rendered')
        run(sys.executable, 'scripts/check_site.py')
