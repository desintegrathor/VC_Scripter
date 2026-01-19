import os
import sys

# Enable switch debugging
os.environ['VCDECOMP_SWITCH_DEBUG'] = '1'

# Run the decompiler
sys.argv = ['vcdecomp', 'structure', 'decompiler_source_tests/test1/tt.scr']
with open('vcdecomp/__main__.py', 'r', encoding='utf-8') as f:
    exec(f.read())
