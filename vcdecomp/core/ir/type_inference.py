"""
Type Inference Engine for Vietcong Script Decompiler.

Aggressively infers variable types from:
1. Instruction patterns (FADD → float, IADD → int)
2. Function call arguments (match against known signatures)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from collections import Counter, defaultdict
from enum import Enum
import logging
import re

from .ssa import SSAFunction, SSAValue, SSAInstruction
from ..headers.database import HeaderDatabase, get_header_database
from ..disasm import opcodes

logger = logging.getLogger(__name__)


class TypePriority(Enum):
    HARD = "hard"
    SOFT = "soft"
    NEUTRAL = "neutral"


class TypeSource(Enum):
    """Source of type evidence."""
    INSTRUCTION = "instruction"
    SEQUENCE_PATTERN = "sequence_pattern"
    FUNCTION_CALL = "function_call"
    STRUCT_ACCESS = "struct_access"
    CONSTANT_VALUE = "constant_value"
    ASSIGNMENT = "assignment"
    SSA_INITIAL = "ssa_initial"  # From stack_lifter opcode inference

    @property
    def priority(self) -> TypePriority:
        return TYPE_SOURCE_PRIORITY[self]


TYPE_SOURCE_PRIORITY = {
    TypeSource.INSTRUCTION: TypePriority.HARD,
    TypeSource.SEQUENCE_PATTERN: TypePriority.NEUTRAL,
    TypeSource.FUNCTION_CALL: TypePriority.HARD,
    TypeSource.STRUCT_ACCESS: TypePriority.HARD,
    TypeSource.CONSTANT_VALUE: TypePriority.SOFT,
    TypeSource.ASSIGNMENT: TypePriority.SOFT,
    TypeSource.SSA_INITIAL: TypePriority.NEUTRAL,
}


@dataclass
class TypeEvidence:
    """Evidence for a variable's type."""

    confidence: float
    """Confidence level (0.0-1.0)"""

    source: TypeSource
    """Where this evidence came from"""

    inferred_type: str
    """The inferred type (e.g., 'int', 'float', 'char*')"""

    distance: int = 0
    """Propagation distance in hops (0 = direct evidence)."""

    reason: str = ""
    """Human-readable explanation"""


@dataclass
class TypeInfo:
    """Collected type information for a variable."""

    var_name: str
    """Variable name (SSA value name or global offset)"""

    evidence: List[TypeEvidence] = field(default_factory=list)
    """All collected evidence"""

    candidate_scores: Dict[str, float] = field(default_factory=dict)
    """Accumulated scores per candidate type"""

    final_type: Optional[str] = None
    """Resolved final type"""

    disallowed_types: Set[str] = field(default_factory=set)
    """Types that must not be selected as final"""

    locked_type: Optional[str] = None
    """Locked type based on high-confidence hard evidence"""

    def add_evidence(self, ev: TypeEvidence):
        """Add new evidence."""
        if self.locked_type and ev.source.priority == TypePriority.SOFT:
            return
        if ev.source.priority == TypePriority.HARD and ev.confidence >= 0.98:
            self.locked_type = ev.inferred_type
        self.evidence.append(ev)
        self.candidate_scores[ev.inferred_type] = (
            self.candidate_scores.get(ev.inferred_type, 0.0) + ev.confidence
        )
        self.final_type = None

    def add_disallowed_type(self, type_name: str) -> None:
        """Register a type that must not be selected."""
        if type_name:
            self.disallowed_types.add(type_name)
            if self.final_type == type_name:
                self.final_type = None

    def has_hard_evidence(self, min_confidence: float = 0.95) -> bool:
        """Check if variable has strong evidence from hard sources."""
        return any(
            ev.confidence >= min_confidence and ev.source.priority == TypePriority.HARD
            for ev in self.evidence
        )

    def prune_candidates(
        self,
        scores: Optional[Dict[str, float]] = None,
        min_ratio: float = 0.1,
        min_score: float = 0.05,
    ) -> Dict[str, float]:
        """
        Remove candidates with very low scores.

        Args:
            scores: Optional score map to prune. If None, prune self.candidate_scores.
            min_ratio: Minimum ratio of the top score required to keep a candidate.
            min_score: Minimum absolute score required to keep a candidate.

        Returns:
            Pruned score map.
        """
        target_scores = scores if scores is not None else self.candidate_scores
        if not target_scores:
            return {} if scores is not None else self.candidate_scores

        max_score = max(target_scores.values())
        threshold = max(min_score, max_score * min_ratio)
        pruned = {name: score for name, score in target_scores.items() if score >= threshold}

        if scores is None:
            self.candidate_scores = pruned
            return self.candidate_scores

        return pruned

    def resolve_type(self) -> str:
        """
        Resolve final type from evidence using weighted voting.

        Returns:
            Best inferred type based on confidence scores
        """
        if not self.evidence and not self.candidate_scores:
            return "int"  # Default fallback

        def score_evidence(evidence: List[TypeEvidence]) -> Dict[str, float]:
            scores: Dict[str, float] = {}
            for ev in evidence:
                scores[ev.inferred_type] = scores.get(ev.inferred_type, 0.0) + ev.confidence
            return scores

        if not self.candidate_scores and self.evidence:
            self.candidate_scores = score_evidence(self.evidence)

        evidence_pool = self.evidence
        if self.has_hard_evidence():
            evidence_pool = [
                ev for ev in self.evidence
                if ev.source.priority != TypePriority.SOFT
            ]

        type_scores = score_evidence(evidence_pool)
        if not type_scores:
            type_scores = dict(self.candidate_scores)

        type_scores = self.prune_candidates(scores=type_scores)

        def filter_disallowed(scores: Dict[str, float]) -> Dict[str, float]:
            if not self.disallowed_types:
                return scores
            return {name: score for name, score in scores.items() if name not in self.disallowed_types}

        hard_confidence_by_type: Dict[str, float] = {}
        for ev in self.evidence:
            if ev.source.priority == TypePriority.HARD:
                hard_confidence_by_type[ev.inferred_type] = max(
                    hard_confidence_by_type.get(ev.inferred_type, 0.0),
                    ev.confidence,
                )

        hard_ban_rules = {
            "float": {"int", "char", "short"},
            "double": {"int", "char", "short", "float"},
            "int": {"float", "double"},
            "short": {"float", "double"},
            "char": {"float", "double"},
        }

        for hard_type, confidence in hard_confidence_by_type.items():
            if confidence < 0.90:
                continue
            for banned in hard_ban_rules.get(hard_type, set()):
                type_scores.pop(banned, None)

        type_scores = filter_disallowed(type_scores)

        if not type_scores:
            type_scores = filter_disallowed(dict(self.candidate_scores))

        if not type_scores:
            for fallback_type in ("int", "short", "char", "void*", "char*", "double", "float"):
                if fallback_type not in self.disallowed_types:
                    self.final_type = fallback_type
                    return self.final_type
            self.final_type = "unknown"
            return self.final_type

        def score_key(type_name: str):
            return (type_scores[type_name], hard_confidence_by_type.get(type_name, 0.0))

        best_type = max(type_scores.keys(), key=score_key)
        self.final_type = best_type
        return self.final_type


@dataclass(frozen=True)
class CallArgumentUsage:
    """Captured call-site argument usage for cross-call aggregation."""

    func_name: str
    arg_index: int
    value: SSAValue
    inferred_type: str
    confidence: float


class TypeInferenceEngine:
    """
    Aggressive type inference for globals and locals.

    Analyzes SSA instructions to infer variable types with high confidence.
    Supports aggressive mode which overrides existing type hints.
    """

    def __init__(self, ssa_func: SSAFunction, aggressive: bool = False, field_tracker=None):
        """
        Initialize type inference engine.

        Args:
            ssa_func: SSA function to analyze
            aggressive: If True, override all types; if False, only infer missing
            field_tracker: Optional FieldAccessTracker instance for struct field type inference
        """
        self.ssa = ssa_func
        self.aggressive = aggressive
        self.header_db = get_header_database()
        self.field_tracker = field_tracker  # Optional FieldAccessTracker for struct accesses

        # SSA value name → TypeInfo
        self.type_info: Dict[str, TypeInfo] = {}
        self._alias_map: Dict[str, List[SSAValue]] = defaultdict(list)
        for value in ssa_func.values.values():
            if value.alias:
                self._alias_map[value.alias].append(value)

        # Context-aware propagation settings
        self.propagation_depth_limit = 10  # Max propagation hops
        self.propagation_min_confidence = 0.70  # Min confidence to propagate
        self.propagation_hop_decay = 0.9  # Exponential confidence decay per hop
        self.max_iterations = 20  # Safety limit for fixed-point iteration

        # Opcode → inferred type mapping
        self._setup_opcode_type_map()
        self._setup_sequence_pattern_map()

        # Cross-call evidence for function arguments
        self._call_argument_evidence: Dict[str, List[TypeEvidence]] = defaultdict(list)
        self._call_argument_usages: Dict[str, List[CallArgumentUsage]] = defaultdict(list)

    def _setup_opcode_type_map(self):
        """Setup mapping from opcodes to type hints."""
        # Float operations
        self.float_ops = {
            'FADD', 'FSUB', 'FMUL', 'FDIV', 'FNEG',
            'FEQ', 'FNE', 'FGT', 'FGE', 'FLT', 'FLE',
            'FSIN', 'FCOS', 'FTAN', 'FSQRT', 'FABS',
        }

        # Integer operations
        self.int_ops = {
            'IADD', 'ISUB', 'IMUL', 'IDIV', 'IMOD', 'INEG',
            'IEQ', 'INE', 'IGT', 'IGE', 'ILT', 'ILE',
            'INC', 'DEC',
        }

        # Character operations
        self.char_ops = {
            'CADD', 'CSUB', 'CMUL', 'CDIV',
            'CEQ', 'CNE', 'CGT', 'CGE', 'CLT', 'CLE',
        }

        # Short operations
        self.short_ops = {
            'SADD', 'SSUB', 'SMUL', 'SDIV',
            'SEQ', 'SNE', 'SGT', 'SGE', 'SLT', 'SLE',
        }

        # Double operations
        self.double_ops = {
            'DADD', 'DSUB', 'DMUL', 'DDIV', 'DNEG',
            'DEQ', 'DNE', 'DGT', 'DGE', 'DLT', 'DLE',
        }

        # Pointer operations
        self.pointer_ops = {
            'PNT', 'DADR', 'LADR', 'GADR',
        }

        # Bitwise and shift operations
        self.bitwise_shift_ops = {
            'BA', 'BO', 'BX', 'BN', 'LS', 'RS',
            'CBA', 'CBX', 'CBO', 'CBN', 'CLS', 'CRS',
            'SBA', 'SBX', 'SBO', 'SBN', 'SLS', 'SRS',
        }

        # Address arithmetic operations
        self.address_arithmetic_ops = {
            'DADR', 'PNT',
        }

        # Type conversion opcodes
        self.conversions = {
            'ITOF': ('int', 'float'),
            'FTOI': ('float', 'int'),
            'FTOD': ('float', 'double'),
            'DTOF': ('double', 'float'),
            'ITOD': ('int', 'double'),
            'DTOI': ('double', 'int'),
            'CTOI': ('char', 'int'),
            'ITOC': ('int', 'char'),
            'STOI': ('short', 'int'),
            'ITOS': ('int', 'short'),
        }

    def _setup_sequence_pattern_map(self) -> None:
        """Setup known instruction sequences that imply operand types."""
        self.sequence_patterns = {
            ('ITOF', 'FADD', 'FTOI'): {
                'expected_type': 'int',
                'confidence': 0.88,
                'reason': 'Integer arithmetic expressed via float add with round-trip conversion',
            },
        }

    def infer_types(self) -> Dict[str, str]:
        """
        Run all inference passes and return resolved types.

        Returns:
            Dictionary mapping variable names to inferred types
        """
        # Run hard-evidence analysis passes
        self._infer_from_instructions()
        self._infer_from_function_calls()
        if self.field_tracker is not None:
            self._infer_from_struct_accesses()

        # Run context-aware data-flow propagation
        self._propagate_through_dataflow()

        # Run soft/heuristic passes after propagation
        self._infer_from_constants()
        self._infer_from_usage_roles()

        # Resolve final types
        return self._resolve_all_types()

    def integrate_with_ssa_values(self) -> None:
        """
        Two-pass integration: collect initial types from SSA, refine via dataflow, write back.

        This method:
        1. Collects initial types from SSA value.value_type fields (from stack_lifter)
        2. Runs full type inference with dataflow propagation
        3. Writes refined types back to SSA value.value_type fields

        The integration uses SSA initial types as evidence with confidence 0.85
        (lower than conversions 0.99 but higher than propagation 0.70).
        """
        # Phase 1: Collect initial types from SSA values as evidence
        self._collect_ssa_initial_types()

        # Phase 2: Run full inference (includes instructions, function calls, propagation)
        inferred_types = self.infer_types()

        # Phase 3: Write refined types back to SSA values
        self._update_ssa_value_types(inferred_types)

    def _collect_ssa_initial_types(self) -> None:
        """Collect initial types from SSA value.value_type fields as evidence."""
        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                # Collect types from outputs
                for value in inst.outputs:
                    if value and value.name and value.value_type != opcodes.ResultType.UNKNOWN:
                        # Map ResultType enum to type string
                        type_str = self._result_type_to_string(value.value_type)
                        if type_str:
                            info = self._get_or_create_type_info(value.name)
                            info.add_evidence(TypeEvidence(
                                confidence=0.85,  # Higher than propagation, lower than conversions
                                source=TypeSource.SSA_INITIAL,
                                inferred_type=type_str,
                                reason=f'Initial type from stack_lifter: {value.value_type.name}'
                            ))

    def _result_type_to_string(self, result_type: opcodes.ResultType) -> Optional[str]:
        """Map opcodes.ResultType enum to type string."""
        mapping = {
            opcodes.ResultType.VOID: None,  # Don't add evidence for void
            opcodes.ResultType.CHAR: 'char',
            opcodes.ResultType.SHORT: 'short',
            opcodes.ResultType.INT: 'int',
            opcodes.ResultType.FLOAT: 'float',
            opcodes.ResultType.DOUBLE: 'double',
            opcodes.ResultType.POINTER: 'void*',  # Generic pointer
            opcodes.ResultType.UNKNOWN: None,  # Don't add evidence for unknown
        }
        return mapping.get(result_type)

    def _update_ssa_value_types(self, inferred_types: Dict[str, str]) -> None:
        """Write refined types back to SSA value.value_type fields."""
        # Reverse mapping: type string to ResultType enum
        type_to_enum = {
            'char': opcodes.ResultType.CHAR,
            'short': opcodes.ResultType.SHORT,
            'int': opcodes.ResultType.INT,
            'float': opcodes.ResultType.FLOAT,
            'double': opcodes.ResultType.DOUBLE,
        }

        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                for value in inst.outputs:
                    if value and value.name and value.name in inferred_types:
                        inferred_type_str = inferred_types[value.name]
                        initial_type = value.value_type

                        # Map string type to ResultType enum
                        refined_type = type_to_enum.get(inferred_type_str, opcodes.ResultType.UNKNOWN)

                        # Update if different and refined is more specific
                        if (
                            refined_type != initial_type
                            and refined_type != opcodes.ResultType.UNKNOWN
                            and self._has_explicit_opcode_evidence(value.name, inferred_type_str)
                        ):
                            # Get confidence for logging
                            info = self.type_info.get(value.name)
                            confidence = info.evidence[-1].confidence if info and info.evidence else 0.0

                            logger.info(
                                f"Type inference refined {value.name}: "
                                f"{initial_type.name} → {refined_type.name} "
                                f"(confidence {confidence:.2f})"
                            )
                            value.value_type = refined_type

    def _has_explicit_opcode_evidence(self, var_name: str, inferred_type: str) -> bool:
        """Check if a variable's type is backed by explicit opcode evidence."""
        info = self.type_info.get(var_name)
        if not info:
            return False

        return any(
            ev.source == TypeSource.INSTRUCTION and ev.inferred_type == inferred_type
            for ev in info.evidence
        )

    def _is_global_value(self, value: SSAValue) -> bool:
        """Return True if SSA value represents a global/data segment reference."""
        if not value or not value.alias:
            return False
        return value.alias.startswith("data_") or value.alias.startswith("&data_")

    def _get_or_create_type_info(self, var_name: str) -> TypeInfo:
        """Get or create TypeInfo for a variable."""
        if var_name not in self.type_info:
            self.type_info[var_name] = TypeInfo(var_name=var_name)
        return self.type_info[var_name]

    def _add_disallowed_type(self, value: Optional[SSAValue], type_name: str) -> None:
        """Add a disallowed type for a value."""
        if value and value.name:
            info = self._get_or_create_type_info(value.name)
            info.add_disallowed_type(type_name)

    def _add_disallowed_types_for_inst(self, inst: SSAInstruction, *type_names: str) -> None:
        """Add disallowed types for all inputs and outputs of an instruction."""
        for value in inst.inputs:
            for type_name in type_names:
                self._add_disallowed_type(value, type_name)
        for value in inst.outputs:
            for type_name in type_names:
                self._add_disallowed_type(value, type_name)

    def _infer_from_instructions(self):
        """Infer types from instruction opcodes."""
        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                self._analyze_instruction(inst)
                if inst.mnemonic in self.bitwise_shift_ops:
                    self._add_disallowed_types_for_inst(inst, 'float')
                if inst.mnemonic in self.address_arithmetic_ops:
                    self._add_disallowed_types_for_inst(inst, 'char*', 'float')
            self._analyze_sequence_patterns(instructions)

    def _analyze_sequence_patterns(self, instructions: List[SSAInstruction]) -> None:
        """Analyze instruction sequences for higher-level type patterns."""
        if not instructions or not self.sequence_patterns:
            return

        for start_idx in range(len(instructions)):
            for pattern, metadata in self.sequence_patterns.items():
                if not self._sequence_matches(instructions, start_idx, pattern):
                    continue
                self._add_sequence_pattern_evidence(
                    instructions[start_idx:start_idx + len(pattern)],
                    pattern,
                    metadata
                )

    def _sequence_matches(
        self,
        instructions: List[SSAInstruction],
        start_idx: int,
        pattern: tuple[str, ...],
    ) -> bool:
        """Check whether a sequence of instructions matches a known pattern."""
        end_idx = start_idx + len(pattern)
        if end_idx > len(instructions):
            return False

        window = instructions[start_idx:end_idx]
        if any(inst.mnemonic != expected for inst, expected in zip(window, pattern)):
            return False

        for prev_inst, next_inst in zip(window, window[1:]):
            if not prev_inst.outputs or not prev_inst.outputs[0]:
                return False
            output_value = prev_inst.outputs[0]
            if not any(output_value == input_val for input_val in next_inst.inputs):
                return False

        return True

    def _add_sequence_pattern_evidence(
        self,
        window: List[SSAInstruction],
        pattern: tuple[str, ...],
        metadata: Dict[str, object],
    ) -> None:
        """Add type evidence based on a matched sequence pattern."""
        expected_type = metadata.get('expected_type')
        confidence = float(metadata.get('confidence', 0.80))
        reason = metadata.get('reason', 'Sequence pattern indicates operand type')

        if not expected_type:
            return

        if pattern == ('ITOF', 'FADD', 'FTOI'):
            itof_inst, _fadd_inst, ftoi_inst = window
            if itof_inst.inputs:
                for input_val in itof_inst.inputs:
                    if input_val and input_val.name:
                        info = self._get_or_create_type_info(input_val.name)
                        info.add_evidence(TypeEvidence(
                            confidence=confidence,
                            source=TypeSource.SEQUENCE_PATTERN,
                            inferred_type=expected_type,
                            reason=reason,
                        ))

            if ftoi_inst.outputs:
                for output_val in ftoi_inst.outputs:
                    if output_val and output_val.name:
                        info = self._get_or_create_type_info(output_val.name)
                        info.add_evidence(TypeEvidence(
                            confidence=confidence,
                            source=TypeSource.SEQUENCE_PATTERN,
                            inferred_type=expected_type,
                            reason=reason,
                        ))

    def _analyze_instruction(self, inst: SSAInstruction):
        """Analyze single instruction for type evidence."""
        mnemonic = inst.mnemonic

        # Float operations
        if mnemonic in self.float_ops:
            self._add_float_evidence(inst)

        # Integer operations
        elif mnemonic in self.int_ops:
            self._add_int_evidence(inst)

        # Character operations
        elif mnemonic in self.char_ops:
            self._add_char_evidence(inst)

        # Short operations
        elif mnemonic in self.short_ops:
            self._add_short_evidence(inst)

        # Double operations
        elif mnemonic in self.double_ops:
            self._add_double_evidence(inst)

        # Type conversions
        elif mnemonic in self.conversions:
            self._add_conversion_evidence(inst)

        # Pointer operations
        elif mnemonic in self.pointer_ops:
            self._add_pointer_evidence(inst)

        # String operations
        elif mnemonic in ['SCPY', 'SCMP', 'SCAT', 'SLEN']:
            self._add_string_evidence(inst)

        # Dereference operations
        elif mnemonic == 'DCP':
            self._add_dereference_evidence(inst)

        # FIX 4: Switch/jump table values are integers
        elif mnemonic in ['JMP', 'JMPI']:
            self._add_switch_evidence(inst)

    def _add_float_evidence(self, inst: SSAInstruction):
        """Add evidence that operands are float."""
        confidence = 0.95  # Very high confidence for float ops

        for value in inst.inputs:
            if value and value.name:
                info = self._get_or_create_type_info(value.name)
                info.add_evidence(TypeEvidence(
                    confidence=confidence,
                    source=TypeSource.INSTRUCTION,
                    inferred_type='float',
                    reason=f'{inst.mnemonic} requires float operands'
                ))

        # Output is also float
        if inst.outputs:
            for value in inst.outputs:
                if value and value.name:
                    info = self._get_or_create_type_info(value.name)
                    info.add_evidence(TypeEvidence(
                        confidence=confidence,
                        source=TypeSource.INSTRUCTION,
                        inferred_type='float',
                        reason=f'{inst.mnemonic} produces float result'
                    ))

    def _add_int_evidence(self, inst: SSAInstruction):
        """Add evidence that operands are int."""
        confidence = 0.90

        for value in inst.inputs:
            if value and value.name:
                info = self._get_or_create_type_info(value.name)
                info.add_evidence(TypeEvidence(
                    confidence=confidence,
                    source=TypeSource.INSTRUCTION,
                    inferred_type='int',
                    reason=f'{inst.mnemonic} requires int operands'
                ))

        if inst.outputs:
            for value in inst.outputs:
                if value and value.name:
                    info = self._get_or_create_type_info(value.name)
                    info.add_evidence(TypeEvidence(
                        confidence=confidence,
                        source=TypeSource.INSTRUCTION,
                        inferred_type='int',
                        reason=f'{inst.mnemonic} produces int result'
                    ))

    def _add_char_evidence(self, inst: SSAInstruction):
        """Add evidence that operands are char."""
        confidence = 0.85

        for value in inst.inputs:
            if value and value.name:
                info = self._get_or_create_type_info(value.name)
                info.add_evidence(TypeEvidence(
                    confidence=confidence,
                    source=TypeSource.INSTRUCTION,
                    inferred_type='char',
                    reason=f'{inst.mnemonic} requires char operands'
                ))

        if inst.outputs:
            for value in inst.outputs:
                if value and value.name:
                    info = self._get_or_create_type_info(value.name)
                    info.add_evidence(TypeEvidence(
                        confidence=confidence,
                        source=TypeSource.INSTRUCTION,
                        inferred_type='char',
                        reason=f'{inst.mnemonic} produces char result'
                    ))

    def _add_short_evidence(self, inst: SSAInstruction):
        """Add evidence that operands are short."""
        confidence = 0.85

        for value in inst.inputs:
            if value and value.name:
                info = self._get_or_create_type_info(value.name)
                info.add_evidence(TypeEvidence(
                    confidence=confidence,
                    source=TypeSource.INSTRUCTION,
                    inferred_type='short',
                    reason=f'{inst.mnemonic} requires short operands'
                ))

        if inst.outputs:
            for value in inst.outputs:
                if value and value.name:
                    info = self._get_or_create_type_info(value.name)
                    info.add_evidence(TypeEvidence(
                        confidence=confidence,
                        source=TypeSource.INSTRUCTION,
                        inferred_type='short',
                        reason=f'{inst.mnemonic} produces short result'
                    ))

    def _add_double_evidence(self, inst: SSAInstruction):
        """Add evidence that operands are double."""
        confidence = 0.95

        for value in inst.inputs:
            if value and value.name:
                info = self._get_or_create_type_info(value.name)
                info.add_evidence(TypeEvidence(
                    confidence=confidence,
                    source=TypeSource.INSTRUCTION,
                    inferred_type='double',
                    reason=f'{inst.mnemonic} requires double operands'
                ))

        if inst.outputs:
            for value in inst.outputs:
                if value and value.name:
                    info = self._get_or_create_type_info(value.name)
                    info.add_evidence(TypeEvidence(
                        confidence=confidence,
                        source=TypeSource.INSTRUCTION,
                        inferred_type='double',
                        reason=f'{inst.mnemonic} produces double result'
                    ))

    def _add_conversion_evidence(self, inst: SSAInstruction):
        """Add evidence from type conversion instructions."""
        from_type, to_type = self.conversions[inst.mnemonic]
        confidence = 0.99  # Conversions are explicit

        # Input is from_type
        if inst.inputs and inst.inputs[0].name:
            info = self._get_or_create_type_info(inst.inputs[0].name)
            info.add_evidence(TypeEvidence(
                confidence=confidence,
                source=TypeSource.INSTRUCTION,
                inferred_type=from_type,
                reason=f'{inst.mnemonic} converts from {from_type}'
            ))

        # Output is to_type
        if inst.outputs and inst.outputs[0].name:
            info = self._get_or_create_type_info(inst.outputs[0].name)
            info.add_evidence(TypeEvidence(
                confidence=confidence,
                source=TypeSource.INSTRUCTION,
                inferred_type=to_type,
                reason=f'{inst.mnemonic} converts to {to_type}'
            ))

    def _add_pointer_evidence(self, inst: SSAInstruction):
        """Add evidence that result is a pointer."""
        confidence = 0.80

        if inst.outputs and inst.outputs[0].name:
            info = self._get_or_create_type_info(inst.outputs[0].name)
            info.add_evidence(TypeEvidence(
                confidence=confidence,
                source=TypeSource.INSTRUCTION,
                inferred_type='void*',  # Generic pointer
                reason=f'{inst.mnemonic} produces pointer'
            ))

    def _add_string_evidence(self, inst: SSAInstruction):
        """Add evidence that operands are strings."""
        confidence = 0.90

        for value in inst.inputs:
            if value and value.name:
                info = self._get_or_create_type_info(value.name)
                info.add_evidence(TypeEvidence(
                    confidence=confidence,
                    source=TypeSource.INSTRUCTION,
                    inferred_type='char*',
                    reason=f'{inst.mnemonic} operates on strings'
                ))

    def _add_dereference_evidence(self, inst: SSAInstruction):
        """Add evidence from dereference operations."""
        # DCP dereferences a pointer
        if inst.inputs and inst.inputs[0].name:
            info = self._get_or_create_type_info(inst.inputs[0].name)
            info.add_evidence(TypeEvidence(
                confidence=0.75,
                source=TypeSource.INSTRUCTION,
                inferred_type='void*',  # Must be pointer
                reason='DCP dereferences pointer'
            ))

    def _add_switch_evidence(self, inst: SSAInstruction):
        """FIX 4: Add evidence that switch/jump table values are integers."""
        # JMP/JMPI use integer index for jump table
        if inst.inputs and inst.inputs[0].name:
            info = self._get_or_create_type_info(inst.inputs[0].name)
            info.add_evidence(TypeEvidence(
                confidence=0.85,
                source=TypeSource.INSTRUCTION,
                inferred_type='int',
                reason='Used as switch/jump table index'
            ))

    def _infer_from_function_calls(self):
        """Infer types from function call arguments."""
        for block_id, instructions in self.ssa.instructions.items():
            for idx, inst in enumerate(instructions):
                if inst.mnemonic == 'XCALL':
                    func_name = self._get_xcall_function_name(inst)
                    if func_name:
                        self._record_call_argument_evidence(func_name, inst.inputs)
                    return_type = self._analyze_function_call(inst)
                    if return_type and return_type not in {'void'}:
                        self._infer_xcall_return_type(instructions, idx, return_type)
        self._apply_call_site_consensus()

    def _get_xcall_function_name(self, inst: SSAInstruction) -> Optional[str]:
        """Extract function name for XCALL instructions."""
        if not inst.instruction or not inst.instruction.instruction:
            return None

        xfn_index = inst.instruction.instruction.arg1
        if not self.ssa.scr.xfn_table:
            return None

        xfn_entries = getattr(self.ssa.scr.xfn_table, 'entries', [])
        if xfn_index >= len(xfn_entries):
            return None

        xfn_entry = xfn_entries[xfn_index]
        if not xfn_entry.name:
            return None

        return xfn_entry.name.split('(')[0] if '(' in xfn_entry.name else xfn_entry.name

    def _record_call_argument_evidence(self, func_name: str, inputs: List[SSAValue]) -> None:
        """Record argument type evidence for a call-site."""
        for arg_index, value in enumerate(inputs):
            if not value or not value.name:
                continue
            inferred = self._infer_argument_type(value)
            if not inferred:
                continue
            inferred_type, confidence = inferred
            evidence = TypeEvidence(
                confidence=confidence,
                source=TypeSource.FUNCTION_CALL,
                inferred_type=inferred_type,
                reason=f'Call-site argument {arg_index} to {func_name}'
            )
            self._call_argument_evidence[func_name].append(evidence)
            self._call_argument_usages[func_name].append(CallArgumentUsage(
                func_name=func_name,
                arg_index=arg_index,
                value=value,
                inferred_type=inferred_type,
                confidence=confidence,
            ))

    def _infer_argument_type(self, value: SSAValue) -> Optional[tuple[str, float]]:
        """Infer the best known type for a call argument."""
        info = self.type_info.get(value.name)
        if info and info.evidence:
            best = max(info.evidence, key=lambda ev: ev.confidence)
            return best.inferred_type, best.confidence

        if value.value_type != opcodes.ResultType.UNKNOWN:
            inferred_type = self._result_type_to_string(value.value_type)
            if inferred_type:
                return inferred_type, 0.80

        return None

    def _apply_call_site_consensus(self) -> None:
        """Aggregate call-site argument evidence and boost consensus types."""
        for func_name, usages in self._call_argument_usages.items():
            per_param: Dict[int, List[CallArgumentUsage]] = defaultdict(list)
            for usage in usages:
                per_param[usage.arg_index].append(usage)

            for arg_index, entries in per_param.items():
                if not entries:
                    continue
                type_counts = Counter(entry.inferred_type for entry in entries)
                if not type_counts:
                    continue

                best_type, best_count = type_counts.most_common(1)[0]
                total = sum(type_counts.values())
                if best_count == total:
                    consensus = "unanimous"
                    consensus_confidence = 0.96
                elif best_count > total / 2:
                    consensus = "majority"
                    consensus_confidence = 0.92
                else:
                    continue

                for entry in entries:
                    if entry.inferred_type != best_type:
                        continue
                    boosted = min(0.99, max(entry.confidence, consensus_confidence))
                    info = self._get_or_create_type_info(entry.value.name)
                    if any(
                        ev.inferred_type == best_type and ev.confidence >= boosted
                        for ev in info.evidence
                    ):
                        continue
                    info.add_evidence(TypeEvidence(
                        confidence=boosted,
                        source=TypeSource.FUNCTION_CALL,
                        inferred_type=best_type,
                        reason=(
                            f'Call-site consensus for {func_name} arg {arg_index} '
                            f'({consensus}: {best_count}/{total})'
                        )
                    ))

    def _analyze_function_call(self, inst: SSAInstruction) -> Optional[str]:
        """Analyze function call for type evidence."""
        func_name = self._get_xcall_function_name(inst)
        if not func_name:
            return None

        # Lookup signature in header database
        func_sig = self.header_db.get_function_signature(func_name)
        if not func_sig:
            return None

        return_type = func_sig.get('return_type')

        # Match arguments to parameter types
        params = func_sig.get('parameters') or []
        param_types = [param[0] for param in params]

        # Inputs to XCALL are the arguments (in reverse order usually)
        for i, value in enumerate(inst.inputs):
            if value and value.name and i < len(param_types):
                param_type = param_types[i]
                info = self._get_or_create_type_info(value.name)
                info.add_evidence(TypeEvidence(
                    confidence=0.98,  # High confidence - header signatures are ground truth from SDK
                    source=TypeSource.FUNCTION_CALL,
                    inferred_type=param_type,
                    reason=f'Passed to {func_name} parameter {i} ({param_type})'
                ))

        if return_type and return_type not in {'void'} and inst.outputs:
            for out_val in inst.outputs:
                if out_val and out_val.name:
                    info = self._get_or_create_type_info(out_val.name)
                    info.add_evidence(TypeEvidence(
                        confidence=0.98,
                        source=TypeSource.FUNCTION_CALL,
                        inferred_type=return_type,
                        reason=f'{func_name} returns {return_type}'
                    ))

        return return_type

    def _infer_xcall_return_type(
        self,
        instructions: List[SSAInstruction],
        xcall_index: int,
        return_type: str
    ) -> None:
        """Infer return types from XCALL + LLD patterns."""
        search_limit = min(len(instructions), xcall_index + 4)
        for next_idx in range(xcall_index + 1, search_limit):
            next_inst = instructions[next_idx]
            if next_inst.mnemonic == "LLD" and next_inst.outputs:
                for out_val in next_inst.outputs:
                    if out_val and out_val.name:
                        info = self._get_or_create_type_info(out_val.name)
                        info.add_evidence(TypeEvidence(
                            confidence=0.96,
                            source=TypeSource.FUNCTION_CALL,
                            inferred_type=return_type,
                            reason='XCALL return value (LLD after XCALL)'
                        ))
                break
            if next_inst.mnemonic in {"CALL", "XCALL", "JMP", "JZ", "JNZ", "RET"}:
                break

    def _infer_from_struct_accesses(self):
        """
        Infer types from struct field accesses.

        If a value represents a struct field access (detected by field_tracker),
        use the field's type from the struct definition.

        Pattern: DCP(PNT(base, offset)) → field type from struct[offset]

        Example:
            // Before: typ info->master_nod is unknown (void*)
            void* master = info->master_nod;

            // After: type is derived from struct definition
            c_Node* master = info->master_nod;  // Because s_SC_OBJ_info.master_nod is c_Node*
        """
        if not self.field_tracker:
            return

        # Import required modules
        from ..structures import get_struct_by_name

        # Iterate over all tracked field accesses
        for ssa_value_name, field_access in self.field_tracker.field_map.items():
            # Get struct definition
            struct_def = get_struct_by_name(field_access.struct_type)
            if not struct_def:
                logger.debug(f"Struct type {field_access.struct_type} not found in registry")
                continue

            # Get field at the offset
            field = struct_def.get_field_at_offset(field_access.field_offset)
            if not field:
                logger.debug(f"No field at offset {field_access.field_offset} in {field_access.struct_type}")
                continue

            # Get field type
            field_type = field.type_name

            # Add evidence for this SSA value
            info = self._get_or_create_type_info(ssa_value_name)
            info.add_evidence(TypeEvidence(
                confidence=0.92,  # High confidence - struct definition is ground truth
                source=TypeSource.STRUCT_ACCESS,
                inferred_type=field_type,
                reason=f'Field {field_access.struct_type}.{field.name} has type {field_type}'
            ))

            logger.debug(
                f"Struct access inference: {ssa_value_name} → {field_type} "
                f"(from {field_access.struct_type}.{field.name})"
            )

    def _infer_from_constants(self):
        """Infer types from constant value ranges."""
        power_of_two_counts: Counter[int] = Counter()
        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                if inst.mnemonic in ['GCP', 'LCP'] and inst.outputs:
                    value = inst.outputs[0]
                    if value and value.alias:
                        int_value = self._parse_int_constant(value.alias)
                        if int_value is not None and self._is_power_of_two(int_value):
                            power_of_two_counts[int_value] += 1

        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                # Check for constant loads (GCP, LCP)
                if inst.mnemonic in ['GCP', 'LCP'] and inst.outputs:
                    value = inst.outputs[0]
                    if value and value.alias:
                        self._infer_from_constant_value(value, power_of_two_counts)

    def _infer_from_constant_value(
        self,
        value: SSAValue,
        power_of_two_counts: Optional[Counter[int]] = None,
    ):
        """Infer type from constant value."""
        if not value.alias:
            return

        alias = value.alias

        # String constant
        if alias.startswith('"') or alias.startswith("'"):
            info = self._get_or_create_type_info(value.name)
            info.add_evidence(TypeEvidence(
                confidence=0.95,
                source=TypeSource.CONSTANT_VALUE,
                inferred_type='char*',
                reason='String literal constant'
            ))
            return

        # Check if it's a numeric constant
        if '.' in alias or 'e' in alias.lower():
            # Float constant (has decimal point)
            confidence = 0.70
            reason_parts = [f'Constant value {alias} has decimal point']
            decimal_match = re.match(r'^-?\d+\.(\d+)$', alias)
            decimal_places = None
            if decimal_match:
                decimal_places = len(decimal_match.group(1))
                if re.match(r'^-?\d+\.\d{1,2}$', alias):
                    confidence = 0.83
                    reason_parts = [f'Constant value {alias} has 1-2 decimal places']
                elif decimal_places >= 3:
                    confidence = 0.60
                    reason_parts = [f'Constant value {alias} has many decimal places']

            if decimal_places is not None and decimal_places <= 1:
                try:
                    float_value = float(alias)
                except ValueError:
                    float_value = None
                if float_value is not None and float_value <= 512.0:
                    confidence = min(confidence + 0.05, 0.95)
                    reason_parts.append('Value <= 512.0 with <=1 decimal place')

            info = self._get_or_create_type_info(value.name)
            info.add_evidence(TypeEvidence(
                confidence=confidence,
                source=TypeSource.CONSTANT_VALUE,
                inferred_type='float',
                reason='; '.join(reason_parts)
            ))
        else:
            int_value = self._parse_int_constant(alias)
            if int_value is None:
                return
            # Integer constant
            val = int_value
            # Check range for char/short/int
            if -128 <= val <= 127:
                type_hint = 'char'
            elif -32768 <= val <= 32767:
                type_hint = 'short'
            else:
                type_hint = 'int'

            info = self._get_or_create_type_info(value.name)
            info.add_evidence(TypeEvidence(
                confidence=0.60,
                source=TypeSource.CONSTANT_VALUE,
                inferred_type=type_hint,
                reason=f'Constant value {alias} fits {type_hint} range'
            ))
            if power_of_two_counts and self._is_power_of_two(val) and power_of_two_counts[val] >= 2:
                flag_confidence = min(0.78 + (power_of_two_counts[val] - 2) * 0.02, 0.90)
                info.add_evidence(TypeEvidence(
                    confidence=flag_confidence,
                    source=TypeSource.CONSTANT_VALUE,
                    inferred_type='int',
                    reason=f'Repeated power-of-two constant {alias} suggests enum/flag int'
                ))

    def _infer_from_usage_roles(self):
        """
        Infer types based on how variables are used (role-based inference).

        Patterns:
        - INC/DEC + comparisons → loop counter → int
        - Used in MUL with constant → array index → int
        - Used in DCP → pointer → void*
        - Used in SCPY/SLEN → string → char*
        """
        bitwise_usage_counts: Counter[str] = Counter()
        bitwise_power_of_two_counts: Counter[str] = Counter()

        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                if inst.mnemonic in self.bitwise_shift_ops:
                    self._add_disallowed_types_for_inst(inst, 'float')
                    for value in inst.inputs + inst.outputs:
                        if value and value.name and not self._is_numeric_constant_alias(value.alias):
                            bitwise_usage_counts[value.name] += 1

                    power_of_two_constants = {
                        self._parse_int_constant(value.alias)
                        for value in inst.inputs
                        if value and value.alias and self._parse_int_constant(value.alias) is not None
                    }
                    power_of_two_constants = {
                        val for val in power_of_two_constants if self._is_power_of_two(val)
                    }
                    if power_of_two_constants:
                        for value in inst.inputs + inst.outputs:
                            if value and value.name and not self._is_numeric_constant_alias(value.alias):
                                bitwise_power_of_two_counts[value.name] += len(power_of_two_constants)

                if inst.mnemonic in self.address_arithmetic_ops:
                    self._add_disallowed_types_for_inst(inst, 'char*', 'float')

                # Loop counter pattern: INC/DEC
                if inst.mnemonic in ['INC', 'DEC']:
                    if inst.outputs and inst.outputs[0].name:
                        info = self._get_or_create_type_info(inst.outputs[0].name)
                        info.add_evidence(TypeEvidence(
                            confidence=0.80,
                            source=TypeSource.INSTRUCTION,
                            inferred_type='int',
                            reason='Used as loop counter (INC/DEC)'
                        ))

                # Array index pattern: MUL with constant
                elif inst.mnemonic in ['IMUL', 'IADD'] and inst.outputs:
                    # Check if used in DADR (array access)
                    output = inst.outputs[0]
                    for user_inst in self._get_users(output):
                        if user_inst.mnemonic == 'DADR':
                            info = self._get_or_create_type_info(output.name)
                            info.add_evidence(TypeEvidence(
                                confidence=0.75,
                                source=TypeSource.INSTRUCTION,
                                inferred_type='int',
                                reason='Used as array index in DADR'
                            ))
                            break

                # Pointer pattern: used in DCP
                elif inst.mnemonic == 'DCP':
                    if inst.inputs and inst.inputs[0].name:
                        info = self._get_or_create_type_info(inst.inputs[0].name)
                        info.add_evidence(TypeEvidence(
                            confidence=0.85,
                            source=TypeSource.INSTRUCTION,
                            inferred_type='void*',
                            reason='Dereferenced with DCP'
                        ))

        for var_name, count in bitwise_usage_counts.items():
            if count >= 2:
                info = self._get_or_create_type_info(var_name)
                confidence = min(0.78 + (count - 2) * 0.02, 0.90)
                info.add_evidence(TypeEvidence(
                    confidence=confidence,
                    source=TypeSource.INSTRUCTION,
                    inferred_type='int',
                    reason='Frequently used in bitwise ops; likely enum/flag int'
                ))
                info.add_disallowed_type('float')

        for var_name, count in bitwise_power_of_two_counts.items():
            if count >= 2:
                info = self._get_or_create_type_info(var_name)
                confidence = min(0.82 + (count - 2) * 0.02, 0.94)
                info.add_evidence(TypeEvidence(
                    confidence=confidence,
                    source=TypeSource.INSTRUCTION,
                    inferred_type='int',
                    reason='Bitwise ops with repeated power-of-two masks suggest enum/flag int'
                ))
                info.add_disallowed_type('float')

    def _parse_int_constant(self, alias: Optional[str]) -> Optional[int]:
        """Parse an integer constant from alias (supports decimal/hex)."""
        if not alias:
            return None
        alias_lower = alias.lower()
        if re.match(r'^-?0x[0-9a-f]+$', alias_lower):
            try:
                return int(alias_lower, 16)
            except ValueError:
                return None
        if re.match(r'^-?\d+$', alias):
            try:
                return int(alias)
            except ValueError:
                return None
        return None

    def _is_numeric_constant_alias(self, alias: Optional[str]) -> bool:
        """Return True if alias looks like a numeric literal."""
        if not alias:
            return False
        if self._parse_int_constant(alias) is not None:
            return True
        return '.' in alias or 'e' in alias.lower()

    @staticmethod
    def _is_power_of_two(value: int) -> bool:
        """Return True for positive powers of two."""
        return value > 0 and (value & (value - 1)) == 0

    def _get_users(self, value: SSAValue) -> List[SSAInstruction]:
        """Get all instructions that use this value as input."""
        users = []
        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                if value in inst.inputs:
                    users.append(inst)
        return users

    def _propagate_through_dataflow(self):
        """
        Main iterative fixed-point algorithm for type propagation.

        Repeats forward + backward passes until no new types are inferred
        or max iterations reached.
        """
        for iteration in range(self.max_iterations):
            changes_made = False

            # Forward propagation: a = b → type flows from b to a
            if self._propagate_forward_pass():
                changes_made = True

            # Backward propagation: FADD(a,b) → a,b must be float
            if self._propagate_backward_pass():
                changes_made = True

            # PHI node merging: PHI(a,b) → merge types
            if self._propagate_phi_pass():
                changes_made = True

            # Converged?
            if not changes_made:
                break

    def _propagate_forward_pass(self) -> bool:
        """
        Forward propagation: type flows from source to destination.

        Patterns:
        - a = b → type(a) = type(b)
        - a = b + 0 → type(a) = type(b)
        - a = NEG(b) → type(a) = type(b)
        - a = DCP(ptr) → type(ptr) = pointer
        - Struct type propagation: if source is s_SC_* or c_*, propagate to target

        Returns:
            True if any new evidence was added
        """
        changes = False

        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                # Simple assignment pattern: a = b
                if inst.mnemonic == 'ASGN' and inst.inputs and inst.outputs:
                    source = inst.inputs[0]
                    dest = inst.outputs[0]
                    if source.name and dest.name:
                        if self._propagate_type_forward(source, dest, 0.90):
                            changes = True
                        # Also try struct type propagation
                        if self._propagate_struct_type(source, dest):
                            changes = True
                elif inst.mnemonic == 'ASGN' and len(inst.inputs) >= 2:
                    source = inst.inputs[0]
                    target = inst.inputs[1]
                    target_alias = target.alias or ""
                    if source.name and target_alias.startswith("&"):
                        target_name = target_alias[1:]
                        source_type = self.get_type_for_variable(source.name)
                        if not source_type and source.value_type != opcodes.ResultType.UNKNOWN:
                            source_type = self._result_type_to_string(source.value_type)
                        if source_type:
                            for target_val in self._alias_map.get(target_name, []):
                                if self._apply_type_constraint(target_val, source_type, 'ASGN'):
                                    changes = True

                # Identity operations: a = b + 0, a = b * 1
                elif self._check_identity_op(inst):
                    source = inst.inputs[0]  # Meaningful operand
                    dest = inst.outputs[0]
                    if source.name and dest.name:
                        if self._propagate_type_forward(source, dest, 0.85):
                            changes = True
                        # Also try struct type propagation
                        if self._propagate_struct_type(source, dest):
                            changes = True

                # Unary operations: NEG, ABS, etc.
                elif inst.mnemonic in ['FNEG', 'INEG', 'CNEG', 'SNEG', 'DNEG']:
                    if inst.inputs and inst.outputs:
                        source = inst.inputs[0]
                        dest = inst.outputs[0]
                        if source.name and dest.name:
                            if self._propagate_type_forward(source, dest, 0.88):
                                changes = True

        return changes

    def _propagate_struct_type(self, source: SSAValue, dest: SSAValue) -> bool:
        """
        Propagate struct types through assignments.

        If source has a struct type (s_SC_* or c_*), propagate it to destination
        with confidence decay.

        Example:
            local_5 = SC_GetPlayer();  // local_5 is s_SC_Player*
            local_6 = local_5;          // local_6 should ALSO be s_SC_Player*

        Args:
            source: Source SSA value
            dest: Destination SSA value

        Returns:
            True if new struct type evidence was added
        """
        if not source.name or not dest.name:
            return False

        source_info = self.type_info.get(source.name)
        if not source_info or not source_info.evidence:
            return False

        # Find struct type in source evidence
        struct_type = None
        struct_confidence = 0.0
        struct_distance = 0

        for ev in source_info.evidence:
            inferred_type = ev.inferred_type
            # Check if this is a struct type (s_SC_*, c_*, or struct pointer)
            if inferred_type and (
                inferred_type.startswith('s_SC_') or
                inferred_type.startswith('s_') or
                inferred_type.startswith('c_') or
                (inferred_type.endswith('*') and ('SC_' in inferred_type or '_' in inferred_type))
            ):
                hops = ev.distance + 1
                if hops > self.propagation_depth_limit:
                    continue
                candidate_confidence = ev.confidence * (self.propagation_hop_decay ** hops)
                if candidate_confidence > struct_confidence:
                    struct_type = inferred_type
                    struct_confidence = candidate_confidence
                    struct_distance = hops

        if not struct_type:
            return False

        propagated_confidence = struct_confidence

        # Check minimum confidence threshold
        if propagated_confidence < self.propagation_min_confidence:
            return False

        if self._is_global_value(dest) and propagated_confidence < 0.95:
            return False

        # Check if destination already has this or better evidence
        dest_info = self._get_or_create_type_info(dest.name)
        if not self._should_accept_evidence(dest_info, TypeSource.ASSIGNMENT):
            return False
        for existing_ev in dest_info.evidence:
            if existing_ev.inferred_type == struct_type:
                if existing_ev.confidence >= propagated_confidence:
                    return False  # Already have equal or better evidence

        # Add propagated struct type evidence
        dest_info.add_evidence(TypeEvidence(
            confidence=propagated_confidence,
            source=TypeSource.ASSIGNMENT,
            inferred_type=struct_type,
            distance=struct_distance,
            reason=f'Struct type propagated from {source.name} (hops={struct_distance})'
        ))

        logger.debug(
            f"Struct type propagation: {source.name} ({struct_type}) → {dest.name} "
            f"(confidence: {struct_confidence:.2f} → {propagated_confidence:.2f}, "
            f"hops={struct_distance})"
        )

        return True

    def _should_accept_evidence(self, dest_info: TypeInfo, source: TypeSource) -> bool:
        """Check if new evidence is allowed based on existing hard types."""
        if dest_info.locked_type and source.priority == TypePriority.SOFT:
            return False
        if dest_info.has_hard_evidence() and source.priority == TypePriority.SOFT:
            return False
        return True

    def _propagate_type_forward(self, source: SSAValue, dest: SSAValue,
                                base_confidence: float) -> bool:
        """
        Propagate type from source to destination.

        Args:
            source: Source SSA value
            dest: Destination SSA value
            base_confidence: Base confidence for this propagation

        Returns:
            True if new evidence was added
        """
        source_info = self.type_info.get(source.name)
        if not source_info or not source_info.evidence:
            return False

        # Get source type
        if not source_info.final_type:
            source_info.resolve_type()

        source_type = source_info.final_type
        if not source_type:
            return False

        propagated_confidence = 0.0
        propagated_distance = 0
        for ev in source_info.evidence:
            if ev.inferred_type != source_type:
                continue
            hops = ev.distance + 1
            if hops > self.propagation_depth_limit:
                continue
            candidate_confidence = min(ev.confidence, base_confidence)
            candidate_confidence *= (self.propagation_hop_decay ** hops)
            if candidate_confidence > propagated_confidence:
                propagated_confidence = candidate_confidence
                propagated_distance = hops

        # Only propagate if source confidence is high enough
        if propagated_confidence < self.propagation_min_confidence:
            return False

        if self._is_global_value(dest) and propagated_confidence < 0.95:
            return False

        # Check if destination already has better evidence
        dest_info = self._get_or_create_type_info(dest.name)
        if not self._should_accept_evidence(dest_info, TypeSource.ASSIGNMENT):
            return False
        for existing_ev in dest_info.evidence:
            if existing_ev.inferred_type == source_type:
                if existing_ev.confidence >= propagated_confidence:
                    return False  # Already have better evidence

        # Add propagated evidence
        dest_info.add_evidence(TypeEvidence(
            confidence=propagated_confidence,
            source=TypeSource.ASSIGNMENT,
            inferred_type=source_type,
            distance=propagated_distance,
            reason=(
                f'Propagated from {source.name} '
                f'(confidence: {propagated_confidence:.2f}, hops={propagated_distance})'
            )
        ))

        return True

    def _check_identity_op(self, inst: SSAInstruction) -> bool:
        """
        Check if instruction is an identity operation (a = b + 0, a = b * 1).

        Args:
            inst: Instruction to check

        Returns:
            True if this is an identity operation
        """
        if inst.mnemonic not in ['IADD', 'ISUB', 'IMUL', 'FADD', 'FSUB', 'FMUL']:
            return False

        if len(inst.inputs) != 2:
            return False

        # Check if second operand is identity constant
        second_operand = inst.inputs[1]
        if not second_operand.alias:
            return False

        # For ADD/SUB: identity is 0
        if inst.mnemonic in ['IADD', 'ISUB', 'FADD', 'FSUB']:
            return second_operand.alias in ['0', '0.0']

        # For MUL: identity is 1
        if inst.mnemonic in ['IMUL', 'FMUL']:
            return second_operand.alias in ['1', '1.0']

        return False

    def _propagate_backward_pass(self) -> bool:
        """
        Backward propagation: type constraints flow from operations to operands.

        Patterns:
        - FADD(a, b) → a,b must be float
        - IADD(a, b) → a,b must be int
        - XCALL with typed params → args must match param types

        Returns:
            True if any new evidence was added
        """
        changes = False

        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                # Get required operand types for this operation
                operand_type = self._get_operand_type_constraint(inst)

                if operand_type:
                    # Apply constraint to all inputs
                    for input_val in inst.inputs:
                        if input_val and input_val.name:
                            if self._apply_type_constraint(input_val, operand_type, inst.mnemonic):
                                changes = True

        return changes

    def _get_operand_type_constraint(self, inst: SSAInstruction) -> Optional[str]:
        """
        Get required operand type for an operation.

        Args:
            inst: Instruction to analyze

        Returns:
            Required type for operands, or None if no constraint
        """
        if inst.mnemonic in self.float_ops:
            return 'float'
        elif inst.mnemonic in self.int_ops:
            return 'int'
        elif inst.mnemonic in self.char_ops:
            return 'char'
        elif inst.mnemonic in self.short_ops:
            return 'short'
        elif inst.mnemonic in self.double_ops:
            return 'double'
        elif inst.mnemonic in ['SCPY', 'SCMP', 'SCAT', 'SLEN']:
            return 'char*'

        return None

    def _apply_type_constraint(self, value: SSAValue, required_type: str,
                              reason_op: str) -> bool:
        """
        Apply type constraint to a value.

        Args:
            value: SSA value to constrain
            required_type: Required type
            reason_op: Operation that requires this type

        Returns:
            True if new evidence was added
        """
        info = self._get_or_create_type_info(value.name)

        # Check if we already have this evidence
        for existing_ev in info.evidence:
            if existing_ev.inferred_type == required_type:
                if existing_ev.confidence >= 0.95:
                    return False  # Already have strong evidence

        # Add constraint evidence
        info.add_evidence(TypeEvidence(
            confidence=0.95,  # High confidence - operation REQUIRES this type
            source=TypeSource.INSTRUCTION,
            inferred_type=required_type,
            reason=f'Required by {reason_op} operation'
        ))

        return True

    def _propagate_phi_pass(self) -> bool:
        """
        Propagate types through PHI nodes (control flow merges).

        Pattern: PHI(a, b, c) → merge types with conflict resolution
        Special handling: Struct types (s_SC_*, c_*) are prioritized

        Returns:
            True if any new evidence was added
        """
        changes = False

        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                if inst.mnemonic != 'PHI':
                    continue

                if not inst.inputs or not inst.outputs:
                    continue

                # Collect types from all PHI inputs
                input_types: Dict[str, float] = {}  # type → max confidence
                struct_types: Dict[str, float] = {}  # struct types separately

                for input_val in inst.inputs:
                    if not input_val or not input_val.name:
                        continue

                    input_info = self.type_info.get(input_val.name)
                    if not input_info or not input_info.evidence:
                        continue

                    # Get type with highest confidence
                    for ev in input_info.evidence:
                        current_conf = input_types.get(ev.inferred_type, 0.0)
                        input_types[ev.inferred_type] = max(current_conf, ev.confidence)

                        # Track struct types separately for priority handling
                        if ev.inferred_type and (
                            ev.inferred_type.startswith('s_SC_') or
                            ev.inferred_type.startswith('s_') or
                            ev.inferred_type.startswith('c_') or
                            (ev.inferred_type.endswith('*') and ('SC_' in ev.inferred_type or '_' in ev.inferred_type))
                        ):
                            struct_conf = struct_types.get(ev.inferred_type, 0.0)
                            struct_types[ev.inferred_type] = max(struct_conf, ev.confidence)

                if not input_types:
                    continue

                # Prefer struct types if available with reasonable confidence
                merged_type = None
                merged_confidence = 0.0

                if struct_types:
                    # Get best struct type
                    best_struct = max(struct_types.items(), key=lambda x: x[1])
                    if best_struct[1] >= 0.70:  # Min confidence for struct type preference
                        merged_type = best_struct[0]
                        merged_confidence = best_struct[1] * 0.90  # 10% penalty for PHI merge (less than normal)

                if not merged_type:
                    # Fall back to dominant type (highest confidence)
                    dominant_type = max(input_types.items(), key=lambda x: x[1])
                    merged_type = dominant_type[0]
                    merged_confidence = dominant_type[1] * 0.85  # 15% penalty for PHI merge

                # Apply to PHI output
                output = inst.outputs[0]
                if output and output.name:
                    if self._is_global_value(output) and merged_confidence < 0.95:
                        continue
                    output_info = self._get_or_create_type_info(output.name)
                    if not self._should_accept_evidence(output_info, TypeSource.INSTRUCTION):
                        continue

                    # Check if we already have this
                    has_evidence = False
                    for ev in output_info.evidence:
                        if ev.inferred_type == merged_type and ev.confidence >= merged_confidence:
                            has_evidence = True
                            break

                    if not has_evidence:
                        output_info.add_evidence(TypeEvidence(
                            confidence=merged_confidence,
                            source=TypeSource.INSTRUCTION,
                            inferred_type=merged_type,
                            reason=f'Merged from PHI inputs ({len(inst.inputs)} paths)'
                        ))
                        changes = True

        return changes

    def _resolve_all_types(self) -> Dict[str, str]:
        """Resolve final types for all variables."""
        resolved = {}
        for var_name, info in self.type_info.items():
            resolved[var_name] = info.resolve_type()
        return resolved

    def get_type_for_variable(self, var_name: str) -> Optional[str]:
        """
        Get inferred type for a specific variable.

        Args:
            var_name: Variable name (SSA value name)

        Returns:
            Inferred type string or None if not inferred
        """
        info = self.type_info.get(var_name)
        if not info:
            return None

        if not info.final_type:
            info.resolve_type()

        return info.final_type

    def get_evidence_for_variable(self, var_name: str) -> List[TypeEvidence]:
        """
        Get all evidence collected for a variable.

        Args:
            var_name: Variable name

        Returns:
            List of evidence entries
        """
        info = self.type_info.get(var_name)
        return info.evidence if info else []

    def dump_type_evidence(self) -> Dict[str, List[Dict[str, object]]]:
        """
        Dump type inference evidence for all variables.

        Returns:
            Mapping of var_name -> list of evidence dictionaries containing
            source, confidence, inferred_type, and reason.
        """
        dump: Dict[str, List[Dict[str, object]]] = {}
        for var_name, info in self.type_info.items():
            evidence_entries = []
            for ev in info.evidence:
                evidence_entries.append({
                    "source": ev.source.value,
                    "confidence": ev.confidence,
                    "inferred_type": ev.inferred_type,
                    "reason": ev.reason,
                })
            dump[var_name] = evidence_entries
        return dump

    def get_confidence(self, var_name: str) -> float:
        """
        Get the maximum confidence score for a variable's type.

        Used by PHI resolution to prefer versions with higher type confidence.

        Args:
            var_name: SSA value name

        Returns:
            Maximum confidence (0.0-1.0), or 0.0 if no evidence
        """
        info = self.type_info.get(var_name)
        if not info or not info.evidence:
            return 0.0
        return max(ev.confidence for ev in info.evidence)

    def get_type_and_confidence(self, var_name: str) -> tuple:
        """
        Get both the inferred type and its confidence for a variable.

        Args:
            var_name: SSA value name

        Returns:
            Tuple of (type_string, confidence) or (None, 0.0) if no evidence
        """
        info = self.type_info.get(var_name)
        if not info or not info.evidence:
            return (None, 0.0)

        # Find evidence with highest confidence
        best_evidence = max(info.evidence, key=lambda ev: ev.confidence)
        return (best_evidence.inferred_type, best_evidence.confidence)

    def infer_parameter_types(self) -> List['ParamInfo']:
        """
        Infer parameter types from function entry and usage patterns.

        This analyzes how parameters are used throughout the function:
        - Function call arguments reveal expected types (XCALL signature matching)
        - Arithmetic operations reveal numeric types (FADD→float, IADD→int)
        - Usage context provides additional evidence

        Returns:
            List of ParamInfo with inferred types, names, and confidence
        """
        # Run full type inference if not already done
        if not self.type_info:
            self.infer_types()

        # Find entry block (usually block 0, but verify)
        entry_block_id = None
        for block_id in sorted(self.ssa.instructions.keys()):
            if block_id >= 0:  # First non-negative block
                entry_block_id = block_id
                break

        if entry_block_id is None:
            return []

        # Collect parameter values from entry block
        # Parameters are identified by LCP instructions with negative offsets
        param_values = self._collect_parameter_values(entry_block_id)

        # Build ParamInfo for each parameter
        param_infos = []
        for idx, param_value in enumerate(param_values):
            # Get inferred type from type inference
            inferred_type = self.get_type_for_variable(param_value.name)
            if not inferred_type:
                inferred_type = 'int'  # Default fallback

            # Get confidence from evidence
            evidence = self.get_evidence_for_variable(param_value.name)
            confidence = self._calculate_confidence(evidence)

            # Get parameter name from save_info if available
            param_name = self._get_parameter_name(idx, param_value.name)

            param_infos.append(ParamInfo(
                index=idx,
                name=param_name,
                type=inferred_type,
                confidence=confidence
            ))

        return param_infos

    def _get_reachable_blocks(self, entry_block_id: int) -> set:
        """
        Get all blocks reachable from entry block (i.e., blocks in this function).

        Uses BFS to find all blocks reachable through CFG edges.
        """
        import sys
        reachable = set()
        queue = [entry_block_id]
        visited = {entry_block_id}

        while queue:
            current_id = queue.pop(0)
            reachable.add(current_id)

            # Get successors from CFG
            current_block = self.ssa.cfg.blocks.get(current_id)
            if not current_block:
                continue

            # Add unvisited successors to queue
            for succ_id in current_block.successors:
                if succ_id not in visited:
                    visited.add(succ_id)
                    queue.append(succ_id)

        return reachable

    def _collect_parameter_values(self, entry_block_id: int) -> List['SSAValue']:
        """
        Collect parameter values from ALL blocks reachable from entry.

        BUGFIX: Parameters may be loaded anywhere in the function, not just entry block.
        But we must only scan blocks that belong to THIS function.
        Parameters are loaded via LCP instructions with negative stack offsets.
        """
        param_values = []
        param_offsets = {}  # offset -> SSAValue

        # Get all blocks reachable from entry (i.e., blocks in this function)
        reachable_blocks = self._get_reachable_blocks(entry_block_id)

        # Scan all reachable blocks for parameter loads
        for block_id in reachable_blocks:
            if block_id not in self.ssa.instructions:
                continue

            for inst in self.ssa.instructions[block_id]:
                # LCP with negative offset = parameter load
                if inst.mnemonic == 'LCP' and inst.instruction:
                    orig_instr = inst.instruction.instruction
                    stack_offset = orig_instr.arg1

                    # Handle two's complement for negative offsets
                    if stack_offset >= 0x80000000:
                        stack_offset = stack_offset - 0x100000000

                    # Negative offset = parameter
                    if stack_offset < 0 and inst.outputs:
                        param_offset = abs(stack_offset)
                        # Only store first occurrence of each offset
                        if param_offset not in param_offsets:
                            param_offsets[param_offset] = inst.outputs[0]

        # Sort by offset to get parameter order
        sorted_offsets = sorted(param_offsets.keys())
        for offset in sorted_offsets:
            param_values.append(param_offsets[offset])

        return param_values

    def _calculate_confidence(self, evidence: List[TypeEvidence]) -> float:
        """Calculate overall confidence from evidence list."""
        if not evidence:
            return 0.0

        # Use weighted average of top 3 evidence items
        sorted_evidence = sorted(evidence, key=lambda e: e.confidence, reverse=True)
        top_evidence = sorted_evidence[:3]

        if not top_evidence:
            return 0.0

        return sum(e.confidence for e in top_evidence) / len(top_evidence)

    def _get_parameter_name(self, param_index: int, ssa_name: str) -> str:
        """
        Get parameter name from save_info debug symbols if available.

        Falls back to param_N if no debug info.
        """
        # Check if save_info exists on scr
        scr = self.ssa.scr
        if hasattr(scr, 'save_info') and scr.save_info and hasattr(scr.save_info, 'parameters'):
            params = scr.save_info.parameters
            if params and param_index < len(params):
                param = params[param_index]
                if hasattr(param, 'name') and param.name:
                    return param.name

        # Fallback: generic name
        return f"param_{param_index}"

    def infer_return_type(self, block_ids: Optional[Set[int]] = None) -> str:
        """
        Infer return type from return statements.

        Analyzes all RET instructions to determine what type is being returned.
        If no values returned, function is void. If values returned, infer
        type from those values.

        Returns:
            Return type string ('void', 'int', 'float', etc.)
        """
        return_values = []
        has_value_return = False

        # Scan all blocks for RET instructions
        blocks = block_ids if block_ids is not None else self.ssa.instructions.keys()
        for block_id in blocks:
            instructions = self.ssa.instructions.get(block_id, [])
            for idx, inst in enumerate(instructions):
                if inst.mnemonic == 'RET':
                    # Look for LLD [sp-3] storing return value before RET
                    for prev_idx in range(idx - 1, max(-1, idx - 6), -1):
                        if prev_idx < 0:
                            break
                        prev_inst = instructions[prev_idx]
                        if prev_inst.mnemonic == 'LLD' and prev_inst.instruction and prev_inst.instruction.instruction:
                            offset = prev_inst.instruction.instruction.arg1
                            if offset >= 0x80000000:
                                offset = offset - 0x100000000
                            if offset == -3 and prev_inst.inputs:
                                has_value_return = True
                                return_values.append(prev_inst.inputs[0])
                                break
                        if prev_inst.mnemonic in {'JMP', 'JZ', 'JNZ', 'CALL', 'XCALL'}:
                            break

        # If ANY RET returns a value, function returns int (not void)
        if not has_value_return:
            return 'void'

        # Infer types of return values if we have them
        if return_values:
            return_types = []
            for value in return_values:
                inferred_type = self.get_type_for_variable(value.name)
                if inferred_type:
                    return_types.append(inferred_type)

            # Merge return types (find dominant type)
            if return_types:
                return self._merge_types(return_types)

        # Default to int if function returns something but we can't determine type
        return 'int'

    def _merge_types(self, types: List[str]) -> str:
        """
        Merge multiple types to find dominant type.

        Rules:
        - If all same, return that type
        - If mix of int/float, prefer float (more general)
        - If mix of pointer types, prefer void*
        - Otherwise return most common type
        """
        if not types:
            return 'int'

        # Count occurrences
        type_counts = {}
        for t in types:
            type_counts[t] = type_counts.get(t, 0) + 1

        # If all same, return it
        if len(type_counts) == 1:
            return types[0]

        # Special rules for numeric types
        if 'float' in type_counts and 'int' in type_counts:
            return 'float'  # Float is more general

        if 'double' in type_counts:
            return 'double'  # Double is most general numeric type

        # Return most common type
        return max(type_counts.items(), key=lambda x: x[1])[0]


@dataclass
class ParamInfo:
    """Parameter information from type inference."""

    index: int
    """Parameter position (0, 1, 2...)"""

    name: str
    """Parameter name (from save_info or generic param_N)"""

    type: str
    """Inferred C type (float, int, c_Node*, etc.)"""

    confidence: float
    """Type inference confidence (0.0-1.0)"""
