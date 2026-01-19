#!/usr/bin/env python3
import os
import sys

# Set environment variable
os.environ['VCDECOMP_SWITCH_DEBUG'] = '1'

# Import and run the decompiler
from vcdecomp.__main__ import main

# Set command-line args
sys.argv = ['vcdecomp', 'structure', 'decompiler_source_tests/test1/tt.scr']

# Run
main()
