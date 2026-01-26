"""
Tests for use-def chain analysis.

This module tests the UseDefChain class which provides foundational
data flow analysis for optimization rules.
"""

import pytest
from vcdecomp.core.ir.ssa import SSAFunction, SSAInstruction, SSAValue
from vcdecomp.core.ir.use_def import UseDefChain, build_use_def_chains
from vcdecomp.core.ir.cfg import CFG, BasicBlock
from vcdecomp.core.disasm import opcodes


@pytest.fixture
def simple_ssa_func():
    """
    Create a simple SSA function for testing:

    Block 0:
        v0 = CONST 42
        v1 = CONST 10
        v2 = ADD v0, v1    # v2 = 42 + 10
        v3 = MUL v2, v0    # v3 = v2 * 42 (v2 used once, v0 used twice)
        XCALL print(v3)

    This tests:
    - Single use (v1, v2)
    - Multiple uses (v0 used in ADD and MUL)
    - Unused output detection
    """
    # Create minimal CFG
    cfg = CFG()
    cfg.blocks[0] = BasicBlock(0, 0, 48, [])  # entry block

    # Create SSA values
    v0 = SSAValue("v0", opcodes.ResultType.INT, producer=0)
    v1 = SSAValue("v1", opcodes.ResultType.INT, producer=12)
    v2 = SSAValue("v2", opcodes.ResultType.INT, producer=24)
    v3 = SSAValue("v3", opcodes.ResultType.INT, producer=36)

    # Create instructions
    inst0 = SSAInstruction(
        block_id=0,
        mnemonic="CONST",
        address=0,
        inputs=[],
        outputs=[v0],
    )
    v0.producer_inst = inst0

    inst1 = SSAInstruction(
        block_id=0,
        mnemonic="CONST",
        address=12,
        inputs=[],
        outputs=[v1],
    )
    v1.producer_inst = inst1

    inst2 = SSAInstruction(
        block_id=0,
        mnemonic="ADD",
        address=24,
        inputs=[v0, v1],
        outputs=[v2],
    )
    v2.producer_inst = inst2

    inst3 = SSAInstruction(
        block_id=0,
        mnemonic="MUL",
        address=36,
        inputs=[v2, v0],
        outputs=[v3],
    )
    v3.producer_inst = inst3

    inst4 = SSAInstruction(
        block_id=0,
        mnemonic="XCALL",
        address=48,
        inputs=[v3],
        outputs=[],
    )

    # Create SSA function
    ssa_func = SSAFunction(
        cfg=cfg,
        values={"v0": v0, "v1": v1, "v2": v2, "v3": v3},
        instructions={0: [inst0, inst1, inst2, inst3, inst4]},
        scr=None,
    )

    return ssa_func


@pytest.fixture
def copy_chain_ssa_func():
    """
    Create SSA function with copy chain for testing copy propagation:

    Block 0:
        v0 = CONST 42
        v1 = COPY v0       # copy
        v2 = COPY v1       # copy chain
        v3 = ADD v2, v2    # use copied value twice
        XCALL print(v3)

    This tests:
    - Copy detection
    - Copy chain tracking
    - Value used multiple times in same instruction
    """
    cfg = CFG()
    cfg.blocks[0] = BasicBlock(0, 0, 48, [])

    v0 = SSAValue("v0", opcodes.ResultType.INT, producer=0)
    v1 = SSAValue("v1", opcodes.ResultType.INT, producer=12)
    v2 = SSAValue("v2", opcodes.ResultType.INT, producer=24)
    v3 = SSAValue("v3", opcodes.ResultType.INT, producer=36)

    inst0 = SSAInstruction(
        block_id=0,
        mnemonic="CONST",
        address=0,
        inputs=[],
        outputs=[v0],
    )
    v0.producer_inst = inst0

    inst1 = SSAInstruction(
        block_id=0,
        mnemonic="COPY",
        address=12,
        inputs=[v0],
        outputs=[v1],
    )
    v1.producer_inst = inst1

    inst2 = SSAInstruction(
        block_id=0,
        mnemonic="COPY",
        address=24,
        inputs=[v1],
        outputs=[v2],
    )
    v2.producer_inst = inst2

    inst3 = SSAInstruction(
        block_id=0,
        mnemonic="ADD",
        address=36,
        inputs=[v2, v2],
        outputs=[v3],
    )
    v3.producer_inst = inst3

    inst4 = SSAInstruction(
        block_id=0,
        mnemonic="XCALL",
        address=48,
        inputs=[v3],
        outputs=[],
    )

    ssa_func = SSAFunction(
        cfg=cfg,
        values={"v0": v0, "v1": v1, "v2": v2, "v3": v3},
        instructions={0: [inst0, inst1, inst2, inst3, inst4]},
        scr=None,
    )

    return ssa_func


class TestUseDefChainConstruction:
    """Test use-def chain construction."""

    def test_builds_without_error(self, simple_ssa_func):
        """Use-def chains should build without errors."""
        chains = UseDefChain(simple_ssa_func)
        assert chains is not None

    def test_convenience_function(self, simple_ssa_func):
        """Convenience function should work."""
        chains = build_use_def_chains(simple_ssa_func)
        assert chains is not None

    def test_tracks_all_values(self, simple_ssa_func):
        """Should track all SSA values."""
        chains = UseDefChain(simple_ssa_func)

        # All values should be tracked
        assert "v0" in chains.defs
        assert "v1" in chains.defs
        assert "v2" in chains.defs
        assert "v3" in chains.defs


class TestDefQueries:
    """Test definition queries."""

    def test_get_def_returns_producer(self, simple_ssa_func):
        """get_def should return the instruction that produces a value."""
        chains = UseDefChain(simple_ssa_func)
        v2 = simple_ssa_func.values["v2"]

        def_inst = chains.get_def(v2)
        assert def_inst is not None
        assert def_inst.mnemonic == "ADD"
        assert def_inst.address == 24

    def test_get_def_for_constant(self, simple_ssa_func):
        """get_def should work for constants."""
        chains = UseDefChain(simple_ssa_func)
        v0 = simple_ssa_func.values["v0"]

        def_inst = chains.get_def(v0)
        assert def_inst is not None
        assert def_inst.mnemonic == "CONST"


class TestUseQueries:
    """Test use queries."""

    def test_get_uses_single_use(self, simple_ssa_func):
        """get_uses should return instructions that use a value (single use case)."""
        chains = UseDefChain(simple_ssa_func)
        v1 = simple_ssa_func.values["v1"]

        uses = chains.get_uses(v1)
        assert len(uses) == 1
        assert uses[0].mnemonic == "ADD"

    def test_get_uses_multiple_uses(self, simple_ssa_func):
        """get_uses should handle multiple uses of same value."""
        chains = UseDefChain(simple_ssa_func)
        v0 = simple_ssa_func.values["v0"]

        uses = chains.get_uses(v0)
        assert len(uses) == 2
        mnemonics = {use.mnemonic for use in uses}
        assert mnemonics == {"ADD", "MUL"}

    def test_use_count(self, simple_ssa_func):
        """use_count should return number of uses."""
        chains = UseDefChain(simple_ssa_func)
        v0 = simple_ssa_func.values["v0"]
        v1 = simple_ssa_func.values["v1"]

        assert chains.use_count(v0) == 2  # used in ADD and MUL
        assert chains.use_count(v1) == 1  # used only in ADD


class TestSingleUseDetection:
    """Test single-use value detection."""

    def test_is_single_use_true(self, simple_ssa_func):
        """is_single_use should return True for values used once."""
        chains = UseDefChain(simple_ssa_func)
        v1 = simple_ssa_func.values["v1"]
        v2 = simple_ssa_func.values["v2"]

        assert chains.is_single_use(v1) is True
        assert chains.is_single_use(v2) is True

    def test_is_single_use_false(self, simple_ssa_func):
        """is_single_use should return False for values used multiple times."""
        chains = UseDefChain(simple_ssa_func)
        v0 = simple_ssa_func.values["v0"]

        assert chains.is_single_use(v0) is False

    def test_get_single_use(self, simple_ssa_func):
        """get_single_use should return the single use instruction."""
        chains = UseDefChain(simple_ssa_func)
        v1 = simple_ssa_func.values["v1"]

        single_use = chains.get_single_use(v1)
        assert single_use is not None
        assert single_use.mnemonic == "ADD"

    def test_get_single_use_returns_none_for_multiple(self, simple_ssa_func):
        """get_single_use should return None if value has multiple uses."""
        chains = UseDefChain(simple_ssa_func)
        v0 = simple_ssa_func.values["v0"]

        single_use = chains.get_single_use(v0)
        assert single_use is None


class TestUnusedDetection:
    """Test unused value detection."""

    def test_is_unused_false_for_used_values(self, simple_ssa_func):
        """is_unused should return False for used values."""
        chains = UseDefChain(simple_ssa_func)
        v0 = simple_ssa_func.values["v0"]

        assert chains.is_unused(v0) is False

    def test_is_unused_true_for_dead_value(self, simple_ssa_func):
        """is_unused should return True for values never used."""
        # Create a dead value by adding an instruction that's never used
        cfg = simple_ssa_func.cfg
        v_dead = SSAValue("v_dead", opcodes.ResultType.INT, producer=100)

        dead_inst = SSAInstruction(
            block_id=0,
            mnemonic="CONST",
            address=100,
            inputs=[],
            outputs=[v_dead],
        )
        v_dead.producer_inst = dead_inst

        simple_ssa_func.values["v_dead"] = v_dead
        simple_ssa_func.instructions[0].append(dead_inst)

        chains = UseDefChain(simple_ssa_func)
        assert chains.is_unused(v_dead) is True


class TestCopyDetection:
    """Test copy instruction detection."""

    def test_is_copy_instruction_true(self, copy_chain_ssa_func):
        """is_copy_instruction should detect COPY instructions."""
        chains = UseDefChain(copy_chain_ssa_func)

        copy_insts = [
            inst
            for block_insts in copy_chain_ssa_func.instructions.values()
            for inst in block_insts
            if inst.mnemonic == "COPY"
        ]

        assert len(copy_insts) == 2
        for copy_inst in copy_insts:
            assert chains.is_copy_instruction(copy_inst) is True

    def test_is_copy_instruction_false(self, copy_chain_ssa_func):
        """is_copy_instruction should return False for non-copy instructions."""
        chains = UseDefChain(copy_chain_ssa_func)

        add_inst = [
            inst
            for block_insts in copy_chain_ssa_func.instructions.values()
            for inst in block_insts
            if inst.mnemonic == "ADD"
        ][0]

        assert chains.is_copy_instruction(add_inst) is False


class TestConstantDetection:
    """Test constant value detection."""

    def test_find_constant_def_from_name(self, simple_ssa_func):
        """Should find constants from value names."""
        chains = UseDefChain(simple_ssa_func)

        # Create a value with constant name
        const_val = SSAValue("const_123", opcodes.ResultType.INT)
        simple_ssa_func.values["const_123"] = const_val

        result = chains.find_constant_def(const_val)
        assert result == 123

    def test_find_constant_def_from_metadata(self, simple_ssa_func):
        """Should find constants from metadata."""
        chains = UseDefChain(simple_ssa_func)
        v0 = simple_ssa_func.values["v0"]
        v0.metadata["constant_value"] = 42

        result = chains.find_constant_def(v0)
        assert result == 42


class TestInstructionQueries:
    """Test instruction-level queries."""

    def test_get_instruction_uses(self, simple_ssa_func):
        """get_instruction_uses should return values used by instruction."""
        chains = UseDefChain(simple_ssa_func)

        # Find the ADD instruction
        add_inst = [
            inst
            for block_insts in simple_ssa_func.instructions.values()
            for inst in block_insts
            if inst.mnemonic == "ADD"
        ][0]

        uses = chains.get_instruction_uses(add_inst)
        assert len(uses) == 2
        assert any(v.name == "v0" for v in uses)
        assert any(v.name == "v1" for v in uses)

    def test_get_instruction_defs(self, simple_ssa_func):
        """get_instruction_defs should return values defined by instruction."""
        chains = UseDefChain(simple_ssa_func)

        # Find the ADD instruction
        add_inst = [
            inst
            for block_insts in simple_ssa_func.instructions.values()
            for inst in block_insts
            if inst.mnemonic == "ADD"
        ][0]

        defs = chains.get_instruction_defs(add_inst)
        assert len(defs) == 1
        assert defs[0].name == "v2"


class TestTransitiveUses:
    """Test transitive use analysis."""

    def test_get_transitive_uses_simple(self, simple_ssa_func):
        """Should find transitive uses through value chain."""
        chains = UseDefChain(simple_ssa_func)
        v0 = simple_ssa_func.values["v0"]

        # v0 is used in:
        # - ADD (direct)
        # - MUL (direct)
        # - XCALL (transitive through v2 -> v3)
        transitive = chains.get_transitive_uses(v0)

        mnemonics = {inst.mnemonic for inst in transitive}
        assert "ADD" in mnemonics
        assert "MUL" in mnemonics
        assert "XCALL" in mnemonics

    def test_get_transitive_uses_copy_chain(self, copy_chain_ssa_func):
        """Should track transitive uses through copy chains."""
        chains = UseDefChain(copy_chain_ssa_func)
        v0 = copy_chain_ssa_func.values["v0"]

        # v0 -> COPY(v1) -> COPY(v2) -> ADD -> XCALL
        transitive = chains.get_transitive_uses(v0)

        mnemonics = {inst.mnemonic for inst in transitive}
        assert "COPY" in mnemonics
        assert "ADD" in mnemonics
        assert "XCALL" in mnemonics


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
