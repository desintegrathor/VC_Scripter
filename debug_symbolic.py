"""Debug script for symbolic resolution analysis."""

import sys
from vcdecomp.core.loader.scr_loader import SCRFile
from vcdecomp.core.ir.ssa import build_ssa_all_blocks
from vcdecomp.core.ir.constant_propagation import ConstantPropagator
from vcdecomp.core.ir.field_tracker import FieldAccessTracker

# Load SCR file
scr_path = "Compiler-testruns/Testrun3/hitable.scr"
with open(scr_path, 'rb') as f:
    scr = SCRFile.from_bytes(f.read())

# Build SSA
ssa = build_ssa_all_blocks(scr)

# Initialize constant propagator
const_prop = ConstantPropagator(ssa)
const_prop.analyze()

print("=== CONSTANT PROPAGATION ANALYSIS ===")
print(f"Data constants: {const_prop.data_constants}")
print(f"\nTracked constants ({len(const_prop.constants)}):")
for name, const_val in sorted(const_prop.constants.items())[:20]:
    print(f"  {name}: {const_val.value} -> {const_val.symbol_name}")

# Initialize field tracker
field_tracker = FieldAccessTracker(ssa, func_name="ScriptMain")
field_tracker.analyze()

print("\n=== FIELD ACCESS TRACKING ===")
print(f"Var struct types: {field_tracker.var_struct_types}")
print(f"Semantic names: {field_tracker.semantic_names}")
print(f"\nTracked field accesses ({len(field_tracker.field_map)}):")
for name, field_access in sorted(field_tracker.field_map.items())[:20]:
    expr = field_tracker.get_field_expression(ssa.values.get(name))
    print(f"  {name}: {expr}")

# Check all instructions in block 10
print("\n=== BLOCK 10 ALL INSTRUCTIONS ===")
if 10 in ssa.instructions:
    for inst in ssa.instructions[10]:
        print(f"{inst.address}: {inst.mnemonic}")
        if inst.inputs:
            print(f"  Inputs: {[f'{v.name}(alias={v.alias})' for v in inst.inputs]}")
        if inst.outputs:
            print(f"  Outputs: {[f'{v.name}(alias={v.alias})' for v in inst.outputs]}")

# Check all DCP instructions in block 10
print("\n=== BLOCK 10 DCP INSTRUCTIONS ===")
if 10 in ssa.instructions:
    for inst in ssa.instructions[10]:
        if inst.mnemonic == "DCP":
            if inst.outputs:
                out = inst.outputs[0]
                print(f"{out.name} (alias={out.alias}) @ {inst.address}:")
                if inst.inputs:
                    inp = inst.inputs[0]
                    print(f"  Input: {inp.name} (alias={inp.alias})")
                    if inp.producer_inst:
                        dadr = inp.producer_inst
                        print(f"  Input producer: {dadr.mnemonic} @ {dadr.address}")
                        if dadr.mnemonic == "DADR" and dadr.instruction and dadr.instruction.instruction:
                            print(f"    DADR offset (arg1): {dadr.instruction.instruction.arg1}")
                        if dadr.inputs:
                            for i, inp2 in enumerate(dadr.inputs):
                                print(f"    DADR input[{i}]: {inp2.name} (alias={inp2.alias})")
                                if inp2.producer_inst:
                                    print(f"      Producer: {inp2.producer_inst.mnemonic} @ {inp2.producer_inst.address}")

# Check specific values
print("\n=== SPECIFIC VALUE CHECK ===")
for value_name in ["t10_0", "t5_0", "t33_0"]:
    if value_name in ssa.values:
        val = ssa.values[value_name]
        print(f"\n{value_name} (alias={val.alias}):")
        const = const_prop.get_constant(val)
        if const:
            print(f"  Constant: {const.value} -> {const.symbol_name}")
        field = field_tracker.get_field_expression(val)
        if field:
            print(f"  Field: {field}")
        if val.producer_inst:
            print(f"  Producer: {val.producer_inst.mnemonic} @ {val.producer_inst.address}")
            # If DCP, show input chain
            if val.producer_inst.mnemonic == "DCP" and val.producer_inst.inputs:
                addr_val = val.producer_inst.inputs[0]
                print(f"    DCP input: {addr_val.name} (alias={addr_val.alias})")
                if addr_val.producer_inst:
                    print(f"      Input producer: {addr_val.producer_inst.mnemonic} @ {addr_val.producer_inst.address}")
                    if addr_val.producer_inst.inputs:
                        for i, inp in enumerate(addr_val.producer_inst.inputs):
                            print(f"        Input[{i}]: {inp.name} (alias={inp.alias})")
