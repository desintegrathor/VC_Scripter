"""Test script to debug switch detection with full logging."""
import logging
import sys

# Enable DEBUG logging for switch detection modules
logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr
)

# Set specific loggers to DEBUG
logging.getLogger('vcdecomp.core.ir.structure.patterns.switch_case').setLevel(logging.DEBUG)
logging.getLogger('vcdecomp.core.ir.structure.analysis.value_trace').setLevel(logging.DEBUG)

# Now run the decompiler
import subprocess
result = subprocess.run(
    [sys.executable, '-m', 'vcdecomp', 'structure', 'decompiler_source_tests/test1/tt.scr'],
    capture_output=True,
    text=True
)

# Output to stdout
print(result.stdout)

# Errors to stderr (will have our debug logs)
if result.stderr:
    print(result.stderr, file=sys.stderr)
