#!/usr/bin/env python3
"""
Extract the compiler opcode map (opcode value -> mnemonic) by correlating
compiled .scr files with their SASM debug listings (.dbg).

Usage:
    python tools/extract_compiler_opcode_map.py

Outputs:
    docs/compiler_opcode_map_partial.json (sorted by opcode)
    Prints coverage statistics to stdout.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vcdecomp.core.loader import SCRFile


def iter_scr_dbg_pairs(root: Path):
    for scr_path in root.rglob("*.scr"):
        dbg_path = scr_path.with_name("sasm.dbg")
        if dbg_path.exists():
            yield scr_path, dbg_path


def parse_dbg_mnemonics(dbg_path: Path) -> list[str]:
    pattern = re.compile(r"\s*(\d+)\s*:\s*([A-Z0-9_]+)")
    mnemonics: list[str] = []
    with dbg_path.open("r", encoding="latin-1") as handle:
        for line in handle:
            match = pattern.match(line)
            if match:
                mnemonics.append(match.group(2))
    return mnemonics


def extract(root: Path) -> dict[int, str]:
    opcode_map: dict[int, str] = {}
    for scr_path, dbg_path in iter_scr_dbg_pairs(root):
        scr = SCRFile.load(str(scr_path), variant="compiler")
        mnemonics = parse_dbg_mnemonics(dbg_path)
        if not mnemonics:
            continue
        limited = mnemonics[: len(scr.code_segment.instructions)]
        for instr, mnemonic in zip(scr.code_segment.instructions, limited):
            opcode_map.setdefault(instr.opcode, mnemonic)
    return opcode_map


def main() -> None:
    root = Path("Compiler-testruns")
    opcode_map = extract(root)
    if not opcode_map:
        raise SystemExit("No opcodes collected – verify Compiler-testruns/* contain .scr + sasm.dbg pairs.")

    output = Path("docs/compiler_opcode_map_partial.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        json.dump({int(opcode): opcode_map[opcode] for opcode in sorted(opcode_map)}, handle, indent=2)

    missing = sorted(set(range(150)) - set(opcode_map))
    print(f"Wrote {output} with {len(opcode_map)} entries.")
    print(f"Missing {len(missing)} opcode ids: {missing}")


if __name__ == "__main__":
    main()
