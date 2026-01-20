"""
Control-flow graph builder for Vietcong SCR bytecode.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from ..loader.scr_loader import SCRFile, Instruction
from ..disasm import opcodes


@dataclass
class BasicBlock:
    block_id: int
    start: int  # first instruction index
    end: int  # last instruction index (inclusive)
    instructions: List[Instruction] = field(default_factory=list)
    successors: Set[int] = field(default_factory=set)  # target block ids
    predecessors: Set[int] = field(default_factory=set)

    def add_successor(self, block_id: int) -> None:
        if block_id >= 0:
            self.successors.add(block_id)


@dataclass
class CFG:
    blocks: Dict[int, BasicBlock]
    entry_block: int
    idom: Dict[int, int] = field(default_factory=dict)
    dom_tree: Dict[int, List[int]] = field(default_factory=dict)
    dom_order: List[int] = field(default_factory=list)

    def get_block(self, block_id: int) -> BasicBlock:
        return self.blocks[block_id]


def _resolve_entry_ip(scr: SCRFile, resolver: opcodes.OpcodeResolver) -> int:
    """
    Resolve the actual entry point address from header.enter_ip.

    Handles special cases:
    - enter_ip >= 0: Use directly as entry point
    - enter_ip == -2: ScriptMain is at address 0
    - enter_ip < -2 (e.g., -112): Detect ScriptMain by finding code after last helper function

    This logic matches the disassembler's entry point detection.
    """
    enter_ip = scr.header.enter_ip

    # Case 1: Positive enter_ip - use directly
    if enter_ip >= 0:
        return enter_ip

    # Case 2: enter_ip == -2 means ScriptMain is at address 0
    if enter_ip == -2:
        return 0

    # Case 3: Negative enter_ip (other than -2) requires detection
    # Find all CALL targets (helper functions)
    call_targets: Set[int] = set()
    internal_call_opcodes = resolver.internal_call_opcodes
    return_opcodes = resolver.return_opcodes
    code_count = scr.code_segment.code_count

    for instr in scr.code_segment.instructions:
        if instr.opcode in internal_call_opcodes:
            call_targets.add(instr.arg1)

    # Find ScriptMain after the last helper function's RET
    if call_targets:
        sorted_call_targets = sorted(call_targets)
        last_helper_start = sorted_call_targets[-1]

        # Find RET after the last helper entry
        for instr in scr.code_segment.instructions:
            if instr.address > last_helper_start and instr.opcode in return_opcodes:
                # RET found, next instruction is potential ScriptMain
                next_addr = instr.address + 1
                if next_addr < code_count:
                    return next_addr
                break

    # Fallback: No helper functions found, ScriptMain is at address 0
    return 0


def build_cfg(scr: SCRFile, resolver: Optional[opcodes.OpcodeResolver] = None) -> CFG:
    """
    Build Control Flow Graph from instructions.

    Basic Block Invariant:
    - Each basic block contains AT MOST ONE control flow instruction (jump/return)
    - If present, it must be the LAST instruction in the block
    - This is enforced by making the instruction after ANY jump/return a block leader
    """
    resolver = resolver or getattr(scr, "opcode_resolver", opcodes.DEFAULT_RESOLVER)
    instructions = scr.code_segment.instructions
    entry_ip = _resolve_entry_ip(scr, resolver)
    leaders: Set[int] = {0, entry_ip}

    for instr in instructions:
        opcode = instr.opcode
        if resolver.is_jump(opcode):
            leaders.add(instr.arg1)
            # Add next instruction as leader after ANY jump (not just conditional)
            # This ensures proper block splitting for consecutive jumps
            next_addr = instr.address + 1
            if next_addr < len(instructions):
                leaders.add(next_addr)
        elif resolver.is_return(opcode):
            next_addr = instr.address + 1
            if next_addr < len(instructions):
                leaders.add(next_addr)

    # Build blocks
    block_starts = sorted(addr for addr in leaders if 0 <= addr < len(instructions))
    blocks: Dict[int, BasicBlock] = {}
    start_to_block: Dict[int, int] = {}

    for block_id, start in enumerate(block_starts):
        end = _find_block_end(start, block_starts, len(instructions))
        block_instructions = instructions[start : end + 1]
        block = BasicBlock(
            block_id=block_id,
            start=start,
            end=end,
            instructions=block_instructions,
        )
        blocks[block_id] = block
        start_to_block[start] = block_id

    # Link successors
    for block in blocks.values():
        last_instr = block.instructions[-1]
        opcode = last_instr.opcode
        if resolver.is_return(opcode):
            continue
        if resolver.is_jump(opcode):
            target_block = start_to_block.get(last_instr.arg1, -1)
            block.add_successor(target_block)
            if resolver.is_conditional_jump(opcode):
                fallthrough = last_instr.address + 1
                block.add_successor(start_to_block.get(fallthrough, -1))
        else:
            fallthrough = last_instr.address + 1
            # Non-jump, non-return instruction - add fallthrough successor
            # If fallthrough is a block leader, link to that block
            # If not, link to the block containing that address
            if fallthrough in start_to_block:
                # Fallthrough is a leader - link to that block
                block.add_successor(start_to_block[fallthrough])
            else:
                # Sequential code - find the block containing fallthrough
                # This handles cases where fallthrough isn't exactly at block start
                for other_block in blocks.values():
                    if other_block.start <= fallthrough <= other_block.end:
                        block.add_successor(other_block.block_id)
                        break

    # Populate predecessors
    for block in blocks.values():
        for succ in block.successors:
            if succ >= 0:
                blocks[succ].predecessors.add(block.block_id)

    # Use the resolved entry_ip from earlier (not raw header.enter_ip)
    entry_block = start_to_block.get(entry_ip, 0)
    cfg = CFG(blocks=blocks, entry_block=entry_block)
    _compute_dominators(cfg)
    return cfg


def _find_block_end(start: int, block_starts: List[int], instr_count: int) -> int:
    idx = block_starts.index(start)
    if idx + 1 < len(block_starts):
        return block_starts[idx + 1] - 1
    return instr_count - 1


def _reverse_postorder(cfg: CFG) -> List[int]:
    visited: Set[int] = set()
    order: List[int] = []

    def dfs(node: int) -> None:
        if node in visited or node not in cfg.blocks:
            return
        visited.add(node)
        for succ in sorted(cfg.blocks[node].successors):
            dfs(succ)
        order.append(node)

    dfs(cfg.entry_block)
    order.reverse()
    return order


def _intersect(idom: Dict[int, int], order_index: Dict[int, int], finger1: int, finger2: int) -> int:
    while finger1 != finger2:
        while order_index[finger1] > order_index[finger2]:
            finger1 = idom[finger1]
        while order_index[finger2] > order_index[finger1]:
            finger2 = idom[finger2]
    return finger1


def _compute_dominators(cfg: CFG) -> None:
    order = _reverse_postorder(cfg)
    if not order:
        return
    order_index = {node: idx for idx, node in enumerate(order)}
    idom: Dict[int, int] = {order[0]: order[0]}
    changed = True

    while changed:
        changed = False
        for node in order[1:]:
            preds = [p for p in cfg.blocks[node].predecessors if p in idom]
            if not preds:
                continue
            new_idom = preds[0]
            for pred in preds[1:]:
                new_idom = _intersect(idom, order_index, pred, new_idom)
            if idom.get(node) != new_idom:
                idom[node] = new_idom
                changed = True

    dom_tree: Dict[int, List[int]] = {node: [] for node in cfg.blocks}
    for node, parent in idom.items():
        if node == parent:
            continue
        dom_tree.setdefault(parent, []).append(node)

    dom_order: List[int] = []

    def dfs(node: int) -> None:
        dom_order.append(node)
        for child in dom_tree.get(node, []):
            dfs(child)

    entry = order[0]
    dfs(entry)

    cfg.idom = idom
    cfg.dom_tree = dom_tree
    cfg.dom_order = dom_order


def dominates(cfg: CFG, dominator: int, node: int) -> bool:
    """Check if 'dominator' dominates 'node'."""
    if dominator == node:
        return True
    current = node
    while current in cfg.idom:
        parent = cfg.idom[current]
        if parent == dominator:
            return True
        if parent == current:
            break
        current = parent
    return False


@dataclass
class BackEdge:
    """A back edge in the CFG (edge from node to its dominator)."""
    source: int  # Node that jumps back
    target: int  # Loop header (dominator)


@dataclass
class NaturalLoop:
    """A natural loop identified by its header and body blocks."""
    header: int  # Loop header block
    body: Set[int]  # All blocks in the loop (including header)
    back_edges: List[BackEdge]  # All back edges to this header
    exits: Set[int]  # Blocks outside the loop that are targets of loop blocks


def find_back_edges(cfg: CFG) -> List[BackEdge]:
    """
    Find all back edges in the CFG.
    A back edge is an edge (source → target) where target dominates source.
    """
    back_edges = []
    for block_id, block in cfg.blocks.items():
        for succ in block.successors:
            if succ in cfg.blocks and dominates(cfg, succ, block_id):
                back_edges.append(BackEdge(source=block_id, target=succ))
    return back_edges


def find_natural_loop(cfg: CFG, back_edge: BackEdge) -> NaturalLoop:
    """
    Find the natural loop for a given back edge.
    The natural loop consists of all nodes that can reach the back edge source
    without going through the header.
    """
    header = back_edge.target
    body: Set[int] = {header}
    worklist = [back_edge.source]

    # Find all nodes that can reach the back edge source without going through header
    while worklist:
        node = worklist.pop()
        if node not in body:
            body.add(node)
            for pred in cfg.blocks[node].predecessors:
                if pred not in body:
                    worklist.append(pred)

    # Find loop exits (successors of loop blocks that are outside the loop)
    exits: Set[int] = set()
    for block_id in body:
        for succ in cfg.blocks[block_id].successors:
            if succ not in body and succ in cfg.blocks:
                exits.add(succ)

    return NaturalLoop(
        header=header,
        body=body,
        back_edges=[back_edge],
        exits=exits
    )


def find_all_loops(cfg: CFG) -> List[NaturalLoop]:
    """
    Find all natural loops in the CFG.
    Merges loops with the same header.
    """
    back_edges = find_back_edges(cfg)
    if not back_edges:
        return []

    # Group back edges by header
    header_to_edges: Dict[int, List[BackEdge]] = {}
    for edge in back_edges:
        header_to_edges.setdefault(edge.target, []).append(edge)

    loops = []
    for header, edges in header_to_edges.items():
        # Find union of all loop bodies for this header
        combined_body: Set[int] = {header}
        for edge in edges:
            loop = find_natural_loop(cfg, edge)
            combined_body.update(loop.body)

        # Find exits for the combined body
        exits: Set[int] = set()
        for block_id in combined_body:
            for succ in cfg.blocks[block_id].successors:
                if succ not in combined_body and succ in cfg.blocks:
                    exits.add(succ)

        loops.append(NaturalLoop(
            header=header,
            body=combined_body,
            back_edges=edges,
            exits=exits
        ))

    # Sort loops by header address (earlier headers first)
    loops.sort(key=lambda l: cfg.blocks[l.header].start)
    return loops


def is_loop_header(cfg: CFG, block_id: int, loops: List[NaturalLoop] = None) -> Optional[NaturalLoop]:
    """Check if a block is a loop header. Returns the loop if found."""
    if loops is None:
        loops = find_all_loops(cfg)
    for loop in loops:
        if loop.header == block_id:
            return loop
    return None


def compute_local_dominators(cfg: CFG, func_blocks: Set[int], entry_block: int) -> Dict[int, int]:
    """
    Compute dominators for a subset of blocks (e.g., a single function).
    Returns idom mapping for the given blocks.
    """
    if entry_block not in func_blocks:
        return {}

    # Build reverse postorder for the subgraph
    visited: Set[int] = set()
    order: List[int] = []

    def dfs(node: int) -> None:
        if node in visited or node not in func_blocks:
            return
        visited.add(node)
        for succ in sorted(cfg.blocks[node].successors):
            if succ in func_blocks:
                dfs(succ)
        order.append(node)

    dfs(entry_block)
    order.reverse()

    if not order:
        return {}

    order_index = {node: idx for idx, node in enumerate(order)}
    idom: Dict[int, int] = {order[0]: order[0]}
    changed = True

    while changed:
        changed = False
        for node in order[1:]:
            preds = [p for p in cfg.blocks[node].predecessors if p in idom and p in func_blocks]
            if not preds:
                continue
            new_idom = preds[0]
            for pred in preds[1:]:
                new_idom = _intersect(idom, order_index, pred, new_idom)
            if idom.get(node) != new_idom:
                idom[node] = new_idom
                changed = True

    return idom


def find_loops_in_function(cfg: CFG, func_blocks: Set[int], entry_block: int) -> List[NaturalLoop]:
    """
    Find all natural loops within a specific function (subset of blocks).
    """
    # Compute local dominators for this function
    local_idom = compute_local_dominators(cfg, func_blocks, entry_block)

    def local_dominates(dominator: int, node: int) -> bool:
        if dominator == node:
            return True
        current = node
        while current in local_idom:
            parent = local_idom[current]
            if parent == dominator:
                return True
            if parent == current:
                break
            current = parent
        return False

    # Find back edges within this function
    back_edges = []
    for block_id in func_blocks:
        block = cfg.blocks[block_id]
        for succ in block.successors:
            if succ in func_blocks and local_dominates(succ, block_id):
                back_edges.append(BackEdge(source=block_id, target=succ))

    if not back_edges:
        return []

    # Group back edges by header and build loops
    header_to_edges: Dict[int, List[BackEdge]] = {}
    for edge in back_edges:
        header_to_edges.setdefault(edge.target, []).append(edge)

    loops = []
    for header, edges in header_to_edges.items():
        combined_body: Set[int] = {header}
        for edge in edges:
            # Find loop body
            body: Set[int] = {header}
            worklist = [edge.source]
            while worklist:
                node = worklist.pop()
                if node not in body and node in func_blocks:
                    body.add(node)
                    for pred in cfg.blocks[node].predecessors:
                        if pred not in body and pred in func_blocks:
                            worklist.append(pred)
            combined_body.update(body)

        exits: Set[int] = set()
        for block_id in combined_body:
            for succ in cfg.blocks[block_id].successors:
                if succ not in combined_body and succ in cfg.blocks:
                    exits.add(succ)

        loops.append(NaturalLoop(
            header=header,
            body=combined_body,
            back_edges=edges,
            exits=exits
        ))

    loops.sort(key=lambda l: cfg.blocks[l.header].start)
    return loops
