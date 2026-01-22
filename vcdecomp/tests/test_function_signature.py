"""
Unit tests for function signature detection.
"""

import unittest
from dataclasses import dataclass, field
from typing import Dict, List

from vcdecomp.core.ir.function_signature import get_function_signature_string


@dataclass
class MockInstruction:
    address: int
    arg1: int = 0


@dataclass
class MockLiftedInstruction:
    instruction: MockInstruction


@dataclass
class MockSSAInstruction:
    mnemonic: str
    inputs: List
    outputs: List
    instruction: MockLiftedInstruction


@dataclass
class MockBlock:
    start: int


@dataclass
class MockCFG:
    blocks: Dict[int, MockBlock]


@dataclass
class MockHeader:
    enter_size: int = 0


@dataclass
class MockScr:
    header: MockHeader = field(default_factory=MockHeader)
    data_segment: object = None


@dataclass
class MockSSAFunction:
    cfg: MockCFG
    instructions: Dict[int, List[MockSSAInstruction]]
    scr: MockScr


class TestFunctionSignatureCallSites(unittest.TestCase):
    def test_no_param_function_uses_void_list(self):
        func_start = 100
        cfg = MockCFG(blocks={
            0: MockBlock(start=0),
            1: MockBlock(start=func_start),
        })
        call_inst = MockSSAInstruction(
            mnemonic="CALL",
            inputs=[],
            outputs=[],
            instruction=MockLiftedInstruction(MockInstruction(address=10, arg1=func_start)),
        )
        ssa_func = MockSSAFunction(
            cfg=cfg,
            instructions={0: [call_inst], 1: []},
            scr=MockScr(),
        )

        signature = get_function_signature_string(
            ssa_func,
            func_name="func_no_params",
            func_start=func_start,
            func_end=None,
            scr_header_enter_size=0,
            type_engine=None,
        )

        self.assertIn("(void)", signature)
        self.assertNotIn("param_0", signature)
        self.assertNotIn("param_1", signature)


if __name__ == "__main__":
    unittest.main()
