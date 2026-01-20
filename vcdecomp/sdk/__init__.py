"""
SDK-based decompiler enhancements.

This package provides functionality to leverage the Vietcong Scripting SDK
to improve decompilation quality through:
- Type inference from function signatures
- Constant recognition (message types, AI modes, etc.)
- Structure field resolution
"""

from .sdk_database import SDKDatabase, FunctionSignature, StructDefinition, StructField

__all__ = ['SDKDatabase', 'FunctionSignature', 'StructDefinition', 'StructField']
