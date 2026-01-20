"""
Liveness Analysis for SSA Variables.

This module computes LIVE_IN and LIVE_OUT sets for each basic block,
enabling proper variable merging during SSA lowering.

Phase 4 of the decompiler improvement plan.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict

from .ssa import SSAFunction, SSAValue, SSAInstruction
from .cfg import CFG


@dataclass
class LivenessInfo:
    """Per-block liveness information."""
    block_id: int
    live_in: Set[str] = field(default_factory=set)   # SSA values live at block entry
    live_out: Set[str] = field(default_factory=set)  # SSA values live at block exit
    use_set: Set[str] = field(default_factory=set)   # Values used before definition in block
    def_set: Set[str] = field(default_factory=set)   # Values defined in block


class LivenessAnalyzer:
    """
    Compute LIVE_IN and LIVE_OUT sets for each basic block.

    Uses iterative dataflow algorithm:
    - LIVE_OUT[B] = union(LIVE_IN[S] for S in successors(B))
    - LIVE_IN[B] = USE[B] ∪ (LIVE_OUT[B] - DEF[B])

    The liveness information is used to build an interference graph,
    which determines which SSA variables can be safely merged into
    a single C variable.
    """

    def __init__(self, ssa_func: SSAFunction, func_block_ids: Set[int]):
        """
        Initialize liveness analyzer.

        Args:
            ssa_func: SSA function representation
            func_block_ids: Set of block IDs belonging to this function
        """
        self.ssa_func = ssa_func
        self.cfg = ssa_func.cfg
        self.func_block_ids = func_block_ids
        self.liveness: Dict[int, LivenessInfo] = {}

    def compute_liveness(self) -> Dict[int, LivenessInfo]:
        """
        Compute liveness information using iterative fixed-point algorithm.

        Returns:
            Dict mapping block_id -> LivenessInfo
        """
        # Step 1: Compute USE and DEF sets for each block
        for block_id in self.func_block_ids:
            use_set, def_set = self._compute_use_def_sets(block_id)
            self.liveness[block_id] = LivenessInfo(
                block_id=block_id,
                use_set=use_set,
                def_set=def_set,
                live_in=set(),
                live_out=set()
            )

        # Step 2: Iterative fixed-point computation
        # Process blocks in reverse postorder for faster convergence
        worklist = list(self.func_block_ids)
        changed = True
        iterations = 0
        max_iterations = 100  # Safety limit

        while changed and iterations < max_iterations:
            changed = False
            iterations += 1

            for block_id in worklist:
                if block_id not in self.liveness:
                    continue

                info = self.liveness[block_id]
                block = self.cfg.blocks.get(block_id)
                if not block:
                    continue

                # Compute LIVE_OUT = union of LIVE_IN of all successors
                new_live_out: Set[str] = set()
                for succ_id in block.successors:
                    if succ_id in self.liveness:
                        new_live_out.update(self.liveness[succ_id].live_in)

                # Compute LIVE_IN = USE ∪ (LIVE_OUT - DEF)
                new_live_in = info.use_set | (new_live_out - info.def_set)

                # Check if anything changed
                if new_live_in != info.live_in or new_live_out != info.live_out:
                    info.live_in = new_live_in
                    info.live_out = new_live_out
                    changed = True

        return self.liveness

    def _compute_use_def_sets(self, block_id: int) -> Tuple[Set[str], Set[str]]:
        """
        Compute USE (upward exposed) and DEF sets for a block.

        USE set: Values that are used before being defined in this block
        DEF set: Values that are defined in this block

        Args:
            block_id: Block ID to analyze

        Returns:
            Tuple of (use_set, def_set)
        """
        use_set: Set[str] = set()
        def_set: Set[str] = set()

        ssa_instrs = self.ssa_func.instructions.get(block_id, [])

        for inst in ssa_instrs:
            # Process inputs (uses) - add to USE if not already in DEF
            for inp in inst.inputs:
                if inp.name and inp.name not in def_set:
                    use_set.add(inp.name)

            # Process outputs (definitions)
            for out in inst.outputs:
                if out.name:
                    def_set.add(out.name)

        return use_set, def_set

    def get_live_at_instruction(self, block_id: int, inst_index: int) -> Set[str]:
        """
        Get the set of variables live at a specific instruction.

        This walks forward from the instruction to the end of the block,
        collecting all variables that are used after this point.

        Args:
            block_id: Block ID
            inst_index: Index of instruction within the block

        Returns:
            Set of live variable names at that point
        """
        if block_id not in self.liveness:
            return set()

        info = self.liveness[block_id]
        ssa_instrs = self.ssa_func.instructions.get(block_id, [])

        if inst_index >= len(ssa_instrs):
            return info.live_out.copy()

        # Start with LIVE_OUT and work backwards to the instruction
        live = info.live_out.copy()

        for i in range(len(ssa_instrs) - 1, inst_index, -1):
            inst = ssa_instrs[i]

            # Remove definitions
            for out in inst.outputs:
                if out.name:
                    live.discard(out.name)

            # Add uses
            for inp in inst.inputs:
                if inp.name:
                    live.add(inp.name)

        return live


@dataclass
class InterferenceEdge:
    """An edge in the interference graph."""
    v1: str
    v2: str

    def __hash__(self):
        # Order-independent hash
        return hash(frozenset([self.v1, self.v2]))

    def __eq__(self, other):
        if not isinstance(other, InterferenceEdge):
            return False
        return {self.v1, self.v2} == {other.v1, other.v2}


class InterferenceGraph:
    """
    Graph where nodes are SSA values and edges connect values
    that are live simultaneously (cannot share a variable).

    Two SSA values interfere if they are both live at the same program point.
    Variables that interfere cannot be merged into the same C variable.
    """

    def __init__(self, liveness: Dict[int, LivenessInfo], ssa_func: SSAFunction):
        """
        Initialize interference graph from liveness information.

        Args:
            liveness: Liveness info for each block
            ssa_func: SSA function for instruction access
        """
        self.nodes: Set[str] = set()
        self.edges: Set[InterferenceEdge] = set()
        self._adjacency: Dict[str, Set[str]] = defaultdict(set)
        self._build_from_liveness(liveness, ssa_func)

    def _build_from_liveness(self, liveness: Dict[int, LivenessInfo], ssa_func: SSAFunction) -> None:
        """
        Build interference edges from live ranges.

        Two variables interfere if they are both live at the same point.
        We check at:
        1. Block entry (LIVE_IN)
        2. Each instruction point within the block
        """
        for block_id, info in liveness.items():
            # At block entry, all LIVE_IN values interfere with each other
            self._add_clique(info.live_in)

            # Walk through block, tracking currently live values
            ssa_instrs = ssa_func.instructions.get(block_id, [])
            live = info.live_in.copy()

            for inst in ssa_instrs:
                # At this point, all live values interfere with new definitions
                # (the new definition is live starting here)
                for out in inst.outputs:
                    if out.name:
                        self.nodes.add(out.name)
                        # The output interferes with everything currently live
                        # EXCEPT its own inputs (they can share the same register)
                        input_names = {inp.name for inp in inst.inputs if inp.name}
                        for live_var in live:
                            if live_var not in input_names:
                                self._add_edge(out.name, live_var)

                # Update liveness: remove definitions, add uses
                for out in inst.outputs:
                    if out.name:
                        live.discard(out.name)
                        live.add(out.name)  # Output is live from here

                for inp in inst.inputs:
                    if inp.name:
                        self.nodes.add(inp.name)
                        live.add(inp.name)

            # At block exit, all LIVE_OUT values interfere
            self._add_clique(info.live_out)

    def _add_clique(self, values: Set[str]) -> None:
        """Add interference edges between all pairs in a set."""
        value_list = list(values)
        for i, v1 in enumerate(value_list):
            self.nodes.add(v1)
            for v2 in value_list[i+1:]:
                self._add_edge(v1, v2)

    def _add_edge(self, v1: str, v2: str) -> None:
        """Add an interference edge between two variables."""
        if v1 == v2:
            return
        edge = InterferenceEdge(v1, v2)
        if edge not in self.edges:
            self.edges.add(edge)
            self._adjacency[v1].add(v2)
            self._adjacency[v2].add(v1)

    def interferes(self, v1: str, v2: str) -> bool:
        """
        Check if two SSA values interfere (cannot share variable).

        Args:
            v1: First SSA value name
            v2: Second SSA value name

        Returns:
            True if they interfere, False if they can be merged
        """
        if v1 == v2:
            return False
        return v2 in self._adjacency.get(v1, set())

    def get_neighbors(self, v: str) -> Set[str]:
        """Get all variables that interfere with the given variable."""
        return self._adjacency.get(v, set()).copy()

    def get_non_interfering_groups(self, values: List[str]) -> List[List[str]]:
        """
        Partition values into groups that can be merged.

        Uses a greedy graph coloring approach to find groups of variables
        that don't interfere with each other.

        Args:
            values: List of SSA value names to partition

        Returns:
            List of groups, where variables in each group can share
            a single C variable
        """
        if not values:
            return []

        # Filter to values that are in the graph
        valid_values = [v for v in values if v in self.nodes or v not in self._adjacency]

        if not valid_values:
            # All values are unknown - they can all be merged
            return [values]

        # Greedy coloring algorithm
        groups: List[List[str]] = []
        assigned: Set[str] = set()

        # Sort by degree (number of interferences) - high degree first
        # This gives better coloring results
        sorted_values = sorted(
            valid_values,
            key=lambda v: len(self._adjacency.get(v, set())),
            reverse=True
        )

        for value in sorted_values:
            if value in assigned:
                continue

            # Find a group where this value doesn't interfere with any member
            placed = False
            for group in groups:
                can_place = True
                for member in group:
                    if self.interferes(value, member):
                        can_place = False
                        break
                if can_place:
                    group.append(value)
                    assigned.add(value)
                    placed = True
                    break

            if not placed:
                # Create new group
                groups.append([value])
                assigned.add(value)

        # Add any values not in the graph to the first group (or new group)
        remaining = [v for v in values if v not in assigned]
        if remaining:
            if groups:
                groups[0].extend(remaining)
            else:
                groups.append(remaining)

        return groups

    def debug_dump(self) -> str:
        """Return a debug string representation of the interference graph."""
        lines = [f"InterferenceGraph: {len(self.nodes)} nodes, {len(self.edges)} edges"]
        for node in sorted(self.nodes):
            neighbors = sorted(self._adjacency.get(node, set()))
            if neighbors:
                lines.append(f"  {node} interferes with: {', '.join(neighbors)}")
        return "\n".join(lines)
