"""
For-loop detection using SSA analysis.

This module implements Ghidra-style for-loop detection by analyzing PHI nodes
in loop headers and identifying initialization and iteration patterns.

Algorithm (from Ghidra's BlockWhileDo::finalTransform):
1. Find PHI node in loop header that merges values from:
   - Initialization block (before loop)
   - Iteration block (loop tail)
2. Verify iteration expression is in loop tail
3. Find initialization expression before loop
4. Convert while loop to for loop

Pattern:
    init_var = initial_value;        // Initializer
    while (condition(init_var)) {    // Header with PHI
        ...                           // Body
        init_var = iterate(init_var); // Iterator in tail
    }

Converts to:
    for (init_var = initial_value; condition(init_var); init_var = iterate(init_var)) {
        ...
    }
"""

from __future__ import annotations

from typing import Optional, Tuple, List, Set, TYPE_CHECKING
from dataclasses import dataclass
import logging

if TYPE_CHECKING:
    from ...ssa import SSAFunction, SSAValue, SSAInstruction
    from ..blocks.hierarchy import BlockWhileDo, StructuredBlock, BlockBasic

logger = logging.getLogger(__name__)


@dataclass
class ForLoopPattern:
    """
    Detected for-loop pattern.

    Stores the components needed to transform a while loop to a for loop.
    """
    loop_variable: str  # Name of the loop variable (PHI output)
    initializer: str    # Initialization expression (e.g., "i = 0")
    iterator: str       # Iteration expression (e.g., "i = i + 1" or "i++")
    phi_node: 'SSAInstruction'  # The PHI node in the header
    init_inst: Optional['SSAInstruction'] = None  # Initialization instruction
    iter_inst: Optional['SSAInstruction'] = None  # Iterator instruction


class ForLoopDetector:
    """
    Detects for-loop patterns in while loops using SSA analysis.

    Uses PHI node analysis to identify loop variables and their
    initialization and iteration patterns.
    """

    def __init__(self, ssa_func: 'SSAFunction'):
        """
        Initialize for-loop detector.

        Args:
            ssa_func: SSA function to analyze
        """
        self.ssa = ssa_func
        self.cfg = ssa_func.cfg

    def detect_for_loop(self, while_block: 'BlockWhileDo') -> Optional[ForLoopPattern]:
        """
        Detect if a while loop can be converted to a for loop.

        Args:
            while_block: The while loop block to analyze

        Returns:
            ForLoopPattern if detected, None otherwise
        """
        if while_block.condition_block is None or while_block.body_block is None:
            return None

        # Get the header block (condition block)
        header = while_block.condition_block
        if not hasattr(header, 'original_block_id'):
            return None

        header_id = header.original_block_id

        # Find PHI nodes in header
        phi_nodes = self._get_phi_nodes(header_id)
        if not phi_nodes:
            logger.debug(f"No PHI nodes in header {header_id}")
            return None

        # Try each PHI node as potential loop variable
        for phi_node in phi_nodes:
            pattern = self._analyze_phi_for_loop_variable(phi_node, while_block)
            if pattern is not None:
                logger.debug(f"Found for-loop pattern: {pattern.loop_variable}")
                return pattern

        return None

    def _get_phi_nodes(self, block_id: int) -> List['SSAInstruction']:
        """Get all PHI nodes in a block."""
        if block_id not in self.ssa.instructions:
            return []

        phi_nodes = []
        for inst in self.ssa.instructions[block_id]:
            if inst.mnemonic == "PHI":
                phi_nodes.append(inst)

        return phi_nodes

    def _analyze_phi_for_loop_variable(
        self,
        phi_node: 'SSAInstruction',
        while_block: 'BlockWhileDo'
    ) -> Optional[ForLoopPattern]:
        """
        Analyze a PHI node to see if it represents a loop variable.

        A loop variable PHI should have:
        - Exactly 2 inputs
        - One from initialization block (before loop)
        - One from iteration block (loop tail)

        Args:
            phi_node: The PHI node to analyze
            while_block: The while loop containing this PHI

        Returns:
            ForLoopPattern if this is a loop variable, None otherwise
        """
        if len(phi_node.inputs) != 2:
            return None

        if len(phi_node.outputs) != 1:
            return None

        loop_var = phi_node.outputs[0]

        # Get the two sources
        # phi_sources: List[Tuple[pred_block_id, source_value]]
        if not loop_var.phi_sources or len(loop_var.phi_sources) != 2:
            return None

        # Identify which is init and which is iterator
        init_source = None
        iter_source = None
        init_block_id = None
        iter_block_id = None

        for pred_id, source_name in loop_var.phi_sources:
            # Get the source value
            if source_name not in self.ssa.values:
                continue

            source_val = self.ssa.values[source_name]

            # Check if this comes from loop tail (iterator)
            if self._is_in_loop_body(pred_id, while_block):
                iter_source = source_val
                iter_block_id = pred_id
            else:
                # Must be from before loop (initializer)
                init_source = source_val
                init_block_id = pred_id

        if init_source is None or iter_source is None:
            logger.debug(f"Could not identify init/iter sources for PHI {phi_node.address}")
            return None

        # Verify iterator is produced in loop tail
        if iter_source.producer is None:
            return None

        # Find the iterator instruction
        iter_inst = iter_source.producer_inst
        if iter_inst is None or iter_inst.block_id != iter_block_id:
            return None

        # Check if iterator references the loop variable (forms a cycle)
        if not self._uses_loop_variable(iter_inst, loop_var.name):
            return None

        # Find the initializer instruction
        init_inst = None
        if init_source.producer is not None:
            init_inst = init_source.producer_inst

        # Build pattern
        pattern = ForLoopPattern(
            loop_variable=loop_var.name,
            initializer=self._format_initializer(init_source, loop_var.name),
            iterator=self._format_iterator(iter_inst, loop_var.name),
            phi_node=phi_node,
            init_inst=init_inst,
            iter_inst=iter_inst,
        )

        return pattern

    def _is_in_loop_body(self, block_id: int, while_block: 'BlockWhileDo') -> bool:
        """
        Check if a block is in the loop body.

        Args:
            block_id: Block ID to check
            while_block: The while loop

        Returns:
            True if block is in loop body
        """
        # Simple heuristic: check if block_id is in covered_blocks of body
        if while_block.body_block is None:
            return False

        return block_id in while_block.body_block.covered_blocks

    def _uses_loop_variable(self, inst: 'SSAInstruction', loop_var_name: str) -> bool:
        """
        Check if an instruction uses the loop variable.

        Args:
            inst: Instruction to check
            loop_var_name: Name of loop variable

        Returns:
            True if instruction uses loop variable
        """
        for input_val in inst.inputs:
            if input_val.name == loop_var_name:
                return True
            # Check if input is an alias of loop var
            if input_val.alias == loop_var_name:
                return True

        return False

    def _format_initializer(self, init_source: 'SSAValue', var_name: str) -> str:
        """
        Format initialization expression.

        Args:
            init_source: The SSA value used for initialization
            var_name: Name of loop variable (for display purposes)

        Returns:
            Formatted initialization string
        """
        # Try to get a simple variable name for display
        display_name = self._get_display_name(var_name)

        # If we have the producer instruction, format it nicely
        if init_source.producer_inst is not None:
            inst = init_source.producer_inst
            expr = self._format_instruction(inst)
            return f"{display_name} = {expr}"

        # Fallback: use the source name
        return f"{display_name} = {init_source.name}"

    def _format_iterator(self, iter_inst: 'SSAInstruction', var_name: str) -> str:
        """
        Format iterator expression.

        Args:
            iter_inst: The iterator instruction
            var_name: Name of loop variable

        Returns:
            Formatted iterator string (e.g., "i++", "i += 1", "i = i + 1")
        """
        display_name = self._get_display_name(var_name)

        # Check for common patterns
        mnemonic = iter_inst.mnemonic

        # Increment: i++
        if mnemonic == "INC" or (mnemonic == "IADD" and self._is_add_one(iter_inst)):
            return f"{display_name}++"

        # Decrement: i--
        if mnemonic == "DEC" or (mnemonic == "ISUB" and self._is_sub_one(iter_inst)):
            return f"{display_name}--"

        # Add: i += n
        if mnemonic == "IADD" and len(iter_inst.inputs) == 2:
            increment = self._get_constant_value(iter_inst.inputs[1])
            if increment is not None:
                return f"{display_name} += {increment}"

        # Subtract: i -= n
        if mnemonic == "ISUB" and len(iter_inst.inputs) == 2:
            decrement = self._get_constant_value(iter_inst.inputs[1])
            if decrement is not None:
                return f"{display_name} -= {decrement}"

        # Fallback: full expression
        expr = self._format_instruction(iter_inst)
        return f"{display_name} = {expr}"

    def _is_add_one(self, inst: 'SSAInstruction') -> bool:
        """Check if instruction is adding 1."""
        if len(inst.inputs) != 2:
            return False

        const_val = self._get_constant_value(inst.inputs[1])
        return const_val == 1

    def _is_sub_one(self, inst: 'SSAInstruction') -> bool:
        """Check if instruction is subtracting 1."""
        if len(inst.inputs) != 2:
            return False

        const_val = self._get_constant_value(inst.inputs[1])
        return const_val == 1

    def _get_constant_value(self, val: 'SSAValue') -> Optional[int]:
        """
        Try to extract a constant value from an SSA value.

        Args:
            val: SSA value to check

        Returns:
            Integer constant if found, None otherwise
        """
        # Check metadata for constant value
        if 'constant' in val.metadata:
            return val.metadata['constant']

        # Check if name indicates constant (e.g., "const_5")
        if val.name.startswith('const_'):
            try:
                return int(val.name.split('_')[1])
            except (IndexError, ValueError):
                pass

        return None

    def _get_display_name(self, ssa_name: str) -> str:
        """
        Get a clean display name for a variable.

        Args:
            ssa_name: SSA variable name

        Returns:
            Clean display name
        """
        # Check for alias
        if ssa_name in self.ssa.values:
            val = self.ssa.values[ssa_name]
            if val.alias:
                return val.alias

        # Try to extract simple name from SSA name
        # e.g., "t100_0" -> "i", "var_5" -> "var_5"
        if ssa_name.startswith('t') and '_' in ssa_name:
            # This is a temp variable, keep it as-is for now
            return ssa_name.split('_')[0]

        return ssa_name

    def _format_instruction(self, inst: 'SSAInstruction') -> str:
        """
        Format an instruction as an expression.

        Args:
            inst: Instruction to format

        Returns:
            Formatted expression string
        """
        mnemonic = inst.mnemonic

        # Binary operations
        if mnemonic in ['IADD', 'FADD']:
            if len(inst.inputs) == 2:
                return f"{inst.inputs[0].name} + {inst.inputs[1].name}"
        elif mnemonic in ['ISUB', 'FSUB']:
            if len(inst.inputs) == 2:
                return f"{inst.inputs[0].name} - {inst.inputs[1].name}"
        elif mnemonic in ['IMUL', 'FMUL']:
            if len(inst.inputs) == 2:
                return f"{inst.inputs[0].name} * {inst.inputs[1].name}"
        elif mnemonic in ['IDIV', 'FDIV']:
            if len(inst.inputs) == 2:
                return f"{inst.inputs[0].name} / {inst.inputs[1].name}"

        # Unary operations
        elif mnemonic == 'INC':
            if len(inst.inputs) == 1:
                return f"{inst.inputs[0].name} + 1"
        elif mnemonic == 'DEC':
            if len(inst.inputs) == 1:
                return f"{inst.inputs[0].name} - 1"

        # Fallback: just show the mnemonic
        inputs_str = ", ".join(inp.name for inp in inst.inputs)
        return f"{mnemonic}({inputs_str})"


def detect_for_loops_in_function(ssa_func: 'SSAFunction') -> dict[int, ForLoopPattern]:
    """
    Detect all for-loop patterns in a function.

    Args:
        ssa_func: SSA function to analyze

    Returns:
        Dictionary mapping block IDs to ForLoopPattern objects
    """
    detector = ForLoopDetector(ssa_func)
    patterns = {}

    # This would need to iterate over all while loops in the structured representation
    # For now, this is a placeholder that would be called per-loop

    return patterns
