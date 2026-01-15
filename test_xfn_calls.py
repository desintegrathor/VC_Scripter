"""Quick test to see which XFN functions are actually called in LEVEL.SCR"""
from vcdecomp.core.loader.scr_loader import SCRFile

# Load the script
scr = SCRFile.load("Compiler-testruns/pilot/LEVEL.SCR")

# Get XCALL opcode
xcall_opcode = None
for opcode, mnemonic in scr.opcode_resolver.opcode_map.items():
    if mnemonic == "XCALL":
        xcall_opcode = opcode
        break

print(f"XCALL opcode: {xcall_opcode}")
print(f"\nTotal XFN functions in table: {scr.xfn_table.xfn_count}")

# Scan code for XCALL instructions
called_xfn_indices = set()
for instr in scr.code_segment.instructions:
    if instr.opcode == xcall_opcode:
        xfn_index = instr.arg1
        if xfn_index < 0x80000000:
            called_xfn_indices.add(xfn_index)

print(f"\nActually called XFN indices: {sorted(called_xfn_indices)}")
print(f"\nActually called XFN functions:")
for idx in sorted(called_xfn_indices):
    xfn = scr.get_xfn(idx)
    if xfn:
        print(f"  [{idx:3d}] {xfn.name}")

# Check for MP functions
print("\n\nChecking for MP/NET functions:")
mp_functions = {'SC_MP_', 'SC_NET_'}
for idx in sorted(called_xfn_indices):
    xfn = scr.get_xfn(idx)
    if xfn:
        func_name = xfn.name.split('(')[0] if '(' in xfn.name else xfn.name
        for prefix in mp_functions:
            if func_name.startswith(prefix):
                print(f"  FOUND MP FUNCTION: [{idx:3d}] {xfn.name}")