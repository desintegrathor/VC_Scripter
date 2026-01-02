"""
Type Inference Engine for Vietcong Script Decompiler.

Aggressively infers variable types from:
1. Instruction patterns (FADD → float, IADD → int)
2. Function call arguments (match against known signatures)
3. Struct field accesses (field type → variable type)
4. Constant values (range-based inference)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from enum import Enum

from .ssa import SSAFunction, SSAValue, SSAInstruction
from ..headers.database import HeaderDatabase, get_header_database


class TypeSource(Enum):
    """Source of type evidence."""
    INSTRUCTION = "instruction"
    FUNCTION_CALL = "function_call"
    STRUCT_ACCESS = "struct_access"
    CONSTANT_VALUE = "constant_value"
    ASSIGNMENT = "assignment"


@dataclass
class TypeEvidence:
    """Evidence for a variable's type."""

    confidence: float
    """Confidence level (0.0-1.0)"""

    source: TypeSource
    """Where this evidence came from"""

    inferred_type: str
    """The inferred type (e.g., 'int', 'float', 'char*')"""

    reason: str = ""
    """Human-readable explanation"""


@dataclass
class TypeInfo:
    """Collected type information for a variable."""

    var_name: str
    """Variable name (SSA value name or global offset)"""

    evidence: List[TypeEvidence] = field(default_factory=list)
    """All collected evidence"""

    final_type: Optional[str] = None
    """Resolved final type"""

    def add_evidence(self, ev: TypeEvidence):
        """Add new evidence."""
        self.evidence.append(ev)

    def resolve_type(self) -> str:
        """
        Resolve final type from evidence using weighted voting.

        Returns:
            Best inferred type based on confidence scores
        """
        if not self.evidence:
            return "int"  # Default fallback

        # Group evidence by type
        type_scores: Dict[str, float] = {}
        for ev in self.evidence:
            if ev.inferred_type not in type_scores:
                type_scores[ev.inferred_type] = 0.0
            type_scores[ev.inferred_type] += ev.confidence

        # Return type with highest total confidence
        best_type = max(type_scores.items(), key=lambda x: x[1])
        self.final_type = best_type[0]
        return self.final_type


class TypeInferenceEngine:
    """
    Aggressive type inference for globals and locals.

    Analyzes SSA instructions to infer variable types with high confidence.
    Supports aggressive mode which overrides existing type hints.
    """

    def __init__(self, ssa_func: SSAFunction, aggressive: bool = True):
        """
        Initialize type inference engine.

        Args:
            ssa_func: SSA function to analyze
            aggressive: If True, override all types; if False, only infer missing
        """
        self.ssa = ssa_func
        self.aggressive = aggressive
        self.header_db = get_header_database()

        # SSA value name → TypeInfo
        self.type_info: Dict[str, TypeInfo] = {}

        # Context-aware propagation settings
        self.propagation_depth_limit = 10  # Max propagation hops
        self.propagation_min_confidence = 0.70  # Min confidence to propagate
        self.propagation_decay = 0.05  # 5% confidence loss per hop
        self.max_iterations = 20  # Safety limit for fixed-point iteration

        # Opcode → inferred type mapping
        self._setup_opcode_type_map()

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

    def infer_types(self) -> Dict[str, str]:
        """
        Run all inference passes and return resolved types.

        Returns:
            Dictionary mapping variable names to inferred types
        """
        # Run pattern-based analysis passes
        self._infer_from_instructions()
        self._infer_from_function_calls()
        self._infer_from_struct_accesses()
        self._infer_from_constants()

        # Run role-based inference before propagation
        self._infer_from_usage_roles()

        # Run context-aware data-flow propagation
        self._propagate_through_dataflow()

        # Resolve final types
        return self._resolve_all_types()

    def _get_or_create_type_info(self, var_name: str) -> TypeInfo:
        """Get or create TypeInfo for a variable."""
        if var_name not in self.type_info:
            self.type_info[var_name] = TypeInfo(var_name=var_name)
        return self.type_info[var_name]

    def _infer_from_instructions(self):
        """Infer types from instruction opcodes."""
        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                self._analyze_instruction(inst)

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

    def _infer_from_function_calls(self):
        """Infer types from function call arguments."""
        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                if inst.mnemonic == 'XCALL':
                    self._analyze_function_call(inst)

    def _analyze_function_call(self, inst: SSAInstruction):
        """Analyze function call for type evidence."""
        if not inst.instruction or not inst.instruction.instruction:
            return

        xfn_index = inst.instruction.instruction.arg1
        if not self.ssa.scr.xfn_table:
            return

        # Get XFN entry
        xfn_entries = getattr(self.ssa.scr.xfn_table, 'entries', [])
        if xfn_index >= len(xfn_entries):
            return

        xfn_entry = xfn_entries[xfn_index]
        if not xfn_entry.name:
            return

        # Extract function name
        func_name = xfn_entry.name.split('(')[0] if '(' in xfn_entry.name else xfn_entry.name

        # Lookup signature in header database
        func_sig = self.header_db.get_function_signature(func_name)
        if not func_sig or not func_sig.get('parameters'):
            return

        # Match arguments to parameter types
        param_types = [param[0] for param in func_sig['parameters']]

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

    def _infer_from_struct_accesses(self):
        """Infer types from struct field accesses."""
        # This requires field tracker integration
        # TODO: Check if field_tracker has type info for accessed fields
        pass

    def _infer_from_constants(self):
        """Infer types from constant value ranges."""
        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                # Check for constant loads (GCP, LCP)
                if inst.mnemonic in ['GCP', 'LCP'] and inst.outputs:
                    value = inst.outputs[0]
                    if value and value.alias:
                        self._infer_from_constant_value(value)

    def _infer_from_constant_value(self, value: SSAValue):
        """Infer type from constant value."""
        if not value.alias:
            return

        alias = value.alias

        # Check if it's a numeric constant
        if alias.replace('-', '').replace('.', '').isdigit():
            # Float constant (has decimal point)
            if '.' in alias or 'e' in alias.lower():
                info = self._get_or_create_type_info(value.name)
                info.add_evidence(TypeEvidence(
                    confidence=0.70,
                    source=TypeSource.CONSTANT_VALUE,
                    inferred_type='float',
                    reason=f'Constant value {alias} has decimal point'
                ))
            # Integer constant
            else:
                val = int(alias)
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

        # String constant
        elif alias.startswith('"') or alias.startswith("'"):
            info = self._get_or_create_type_info(value.name)
            info.add_evidence(TypeEvidence(
                confidence=0.95,
                source=TypeSource.CONSTANT_VALUE,
                inferred_type='char*',
                reason='String literal constant'
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
        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
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

                # Identity operations: a = b + 0, a = b * 1
                elif self._check_identity_op(inst):
                    source = inst.inputs[0]  # Meaningful operand
                    dest = inst.outputs[0]
                    if source.name and dest.name:
                        if self._propagate_type_forward(source, dest, 0.85):
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

        # Get max confidence from source evidence
        max_source_confidence = max(ev.confidence for ev in source_info.evidence)

        # Only propagate if source confidence is high enough
        if max_source_confidence < self.propagation_min_confidence:
            return False

        # Get source type
        if not source_info.final_type:
            source_info.resolve_type()

        source_type = source_info.final_type
        if not source_type:
            return False

        # Apply confidence decay
        propagated_confidence = max_source_confidence * (1.0 - self.propagation_decay)
        propagated_confidence = min(propagated_confidence, base_confidence)

        # Check if destination already has better evidence
        dest_info = self._get_or_create_type_info(dest.name)
        for existing_ev in dest_info.evidence:
            if existing_ev.inferred_type == source_type:
                if existing_ev.confidence >= propagated_confidence:
                    return False  # Already have better evidence

        # Add propagated evidence
        dest_info.add_evidence(TypeEvidence(
            confidence=propagated_confidence,
            source=TypeSource.ASSIGNMENT,
            inferred_type=source_type,
            reason=f'Propagated from {source.name} (confidence: {max_source_confidence:.2f})'
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

                if not input_types:
                    continue

                # Get dominant type (highest total confidence)
                dominant_type = max(input_types.items(), key=lambda x: x[1])
                merged_type = dominant_type[0]
                merged_confidence = dominant_type[1] * 0.85  # 15% penalty for PHI merge

                # Apply to PHI output
                output = inst.outputs[0]
                if output and output.name:
                    output_info = self._get_or_create_type_info(output.name)

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
