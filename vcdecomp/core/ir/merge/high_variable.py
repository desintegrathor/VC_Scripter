"""
HighVariable - merged source-level variable representation.

This module provides the HighVariable class which represents a single
source-level variable that may encompass multiple SSA values.

Modeled after Ghidra's HighVariable in high.hh - multiple SSA versions
(Varnodes in Ghidra terms) are merged into one HighVariable when they
represent the same source variable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

from .cover import Cover

if TYPE_CHECKING:
    from ...ssa import SSAValue
    from ...disasm.opcodes import ResultType


@dataclass
class HighVariable:
    """
    A high-level source variable merging multiple SSA values.

    Attributes:
        name: Display name for the variable
        instances: List of SSA values merged into this variable
        cover: Combined cover (live range) of all instances
        data_type: Inferred data type
        is_parameter: Whether this is a function parameter
        is_global: Whether this is a global variable
    """
    name: str
    instances: List["SSAValue"] = field(default_factory=list)
    cover: Cover = field(default_factory=Cover)
    data_type: Optional["ResultType"] = None
    is_parameter: bool = False
    is_global: bool = False
    stack_offset: Optional[int] = None  # For locals

    def add_instance(self, value: "SSAValue", value_cover: Cover):
        """
        Add an SSA value instance to this HighVariable.

        Args:
            value: The SSA value to add
            value_cover: The cover for the value
        """
        self.instances.append(value)
        self.cover.merge(value_cover)

        # Update type if not set
        if self.data_type is None and hasattr(value, 'value_type'):
            self.data_type = value.value_type

    def can_merge(self, other: "HighVariable") -> bool:
        """
        Check if another HighVariable can be merged into this one.

        Merging is allowed if:
        1. Covers don't intersect (values aren't live at same time)
        2. Types are compatible
        3. Both are same category (local/global/parameter)
        """
        # Covers must not intersect
        if self.cover.intersects(other.cover):
            return False

        # Categories must match
        if self.is_global != other.is_global:
            return False
        if self.is_parameter != other.is_parameter:
            return False

        # Stack offset must match for locals
        if self.stack_offset is not None and other.stack_offset is not None:
            if self.stack_offset != other.stack_offset:
                return False

        # Types should be compatible (both None or same)
        if self.data_type is not None and other.data_type is not None:
            if self.data_type != other.data_type:
                return False

        return True

    def merge(self, other: "HighVariable"):
        """
        Merge another HighVariable into this one.

        Assumes can_merge() returned True.
        """
        for instance in other.instances:
            self.instances.append(instance)

        self.cover.merge(other.cover)

        # Take type from other if we don't have one
        if self.data_type is None:
            self.data_type = other.data_type

    def get_best_name(self) -> str:
        """
        Get the best display name for this variable.

        Prefers:
        1. Explicit alias if set
        2. Name derived from stack offset
        3. First instance name
        4. Fallback to self.name
        """
        # Check instances for alias
        for inst in self.instances:
            if hasattr(inst, 'alias') and inst.alias:
                return inst.alias

        # Check for typed name
        for inst in self.instances:
            if hasattr(inst, 'name') and not inst.name.startswith('t'):
                return inst.name

        return self.name

    def get_declaration(self) -> str:
        """
        Get a declaration string for this variable.

        Returns something like "int x" or "float y".
        """
        type_str = "dword"  # Default
        if self.data_type is not None:
            type_str = self.data_type.name.lower()

        name = self.get_best_name()
        return f"{type_str} {name}"


def create_high_variable(
    value: "SSAValue",
    cover: Cover,
    name: Optional[str] = None
) -> HighVariable:
    """
    Create a HighVariable from a single SSA value.

    Args:
        value: The SSA value
        cover: The cover for the value
        name: Optional name override

    Returns:
        New HighVariable containing this value
    """
    var_name = name
    if var_name is None:
        if hasattr(value, 'alias') and value.alias:
            var_name = value.alias
        elif hasattr(value, 'name'):
            var_name = value.name
        else:
            var_name = "var"

    hv = HighVariable(name=var_name)
    hv.add_instance(value, cover)

    # Set properties from value metadata
    if hasattr(value, 'value_type'):
        hv.data_type = value.value_type

    if hasattr(value, 'metadata'):
        meta = value.metadata
        hv.is_parameter = meta.get('is_parameter', False)
        hv.is_global = meta.get('is_global', False)
        hv.stack_offset = meta.get('stack_offset')

    return hv
