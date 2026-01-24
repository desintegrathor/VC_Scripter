"""
Tests for the sc_global.h parser.
"""

import pytest
from pathlib import Path

from vcdecomp.core.headers.sc_global_parser import (
    SCGlobalParser,
    parse_sc_global_header,
    get_struct_definitions,
    get_function_struct_params,
)


class TestSCGlobalParser:
    """Tests for SCGlobalParser class."""

    def test_parse_basic_struct(self):
        """Test parsing a simple struct definition."""
        parser = SCGlobalParser()
        content = '''
typedef struct{
    float x,y,z;
}c_Vector3;
'''
        parser._parse_defines(content)
        parser._parse_structs(content)

        assert 'c_Vector3' in parser.structs
        struct = parser.structs['c_Vector3']
        assert len(struct.fields) == 3
        assert struct.fields[0].name == 'x'
        assert struct.fields[0].offset == 0
        assert struct.fields[1].name == 'y'
        assert struct.fields[1].offset == 4
        assert struct.fields[2].name == 'z'
        assert struct.fields[2].offset == 8

    def test_parse_struct_with_pointer(self):
        """Test parsing struct with pointer fields."""
        parser = SCGlobalParser()
        content = '''
typedef struct{
    char *name;
    void *data;
}s_test;
'''
        parser._parse_defines(content)
        parser._parse_structs(content)

        assert 's_test' in parser.structs
        struct = parser.structs['s_test']
        assert len(struct.fields) == 2
        assert struct.fields[0].is_pointer
        assert struct.fields[1].is_pointer

    def test_parse_struct_with_array(self):
        """Test parsing struct with array fields."""
        parser = SCGlobalParser()
        content = '''
#define MAX_SIZE 8
typedef struct{
    dword items[MAX_SIZE];
    dword count;
}s_array_test;
'''
        parser._parse_defines(content)
        parser._parse_structs(content)

        assert 's_array_test' in parser.structs
        struct = parser.structs['s_array_test']
        assert len(struct.fields) == 2
        assert struct.fields[0].is_array
        assert struct.fields[0].array_size == 8
        # Array of 8 dwords = 32 bytes, then count at offset 32
        assert struct.fields[1].offset == 32

    def test_parse_extern_function(self):
        """Test parsing extern function declarations."""
        parser = SCGlobalParser()
        content = '''
extern void SC_P_Create(s_SC_P_Create *info);
extern void SC_P_GetPos(dword pl_id, c_Vector3 *pos);
'''
        parser._parse_functions(content)

        assert 'SC_P_Create' in parser.functions
        func = parser.functions['SC_P_Create']
        assert func.struct_params == {0: 's_SC_P_Create'}

        assert 'SC_P_GetPos' in parser.functions
        func = parser.functions['SC_P_GetPos']
        assert func.struct_params == {1: 'c_Vector3'}

    def test_parse_function_multiple_struct_params(self):
        """Test parsing function with multiple struct parameters."""
        parser = SCGlobalParser()
        content = '''
extern BOOL SC_IsNear3D(c_Vector3 *a, c_Vector3 *b, float dist);
'''
        parser._parse_functions(content)

        assert 'SC_IsNear3D' in parser.functions
        func = parser.functions['SC_IsNear3D']
        assert func.struct_params == {0: 'c_Vector3', 1: 'c_Vector3'}


class TestParseScGlobalHeader:
    """Tests for parse_sc_global_header function."""

    def test_parses_real_header(self):
        """Test that the real sc_global.h can be parsed."""
        header_path = Path(__file__).parent.parent / 'compiler' / 'inc' / 'sc_global.h'
        if not header_path.exists():
            pytest.skip("sc_global.h not found")

        structs, funcs = parse_sc_global_header(str(header_path))

        # Should have found many structs and functions
        assert len(structs) > 40
        assert len(funcs) > 50

    def test_known_structs_present(self):
        """Test that known structs are parsed correctly."""
        structs = get_struct_definitions()

        # Check c_Vector3
        assert 'c_Vector3' in structs
        fields = structs['c_Vector3']
        assert any(f[1] == 'x' for f in fields)
        assert any(f[1] == 'y' for f in fields)
        assert any(f[1] == 'z' for f in fields)

        # Check s_SC_initside
        assert 's_SC_initside' in structs
        fields = structs['s_SC_initside']
        field_names = [f[1] for f in fields]
        assert 'MaxHideOutsStatus' in field_names
        assert 'MaxGroups' in field_names

        # Check s_SC_initgroup
        assert 's_SC_initgroup' in structs
        fields = structs['s_SC_initgroup']
        field_names = [f[1] for f in fields]
        assert 'SideId' in field_names
        assert 'GroupId' in field_names
        assert 'MaxPlayers' in field_names

    def test_known_functions_present(self):
        """Test that known functions are parsed correctly."""
        funcs = get_function_struct_params()

        # Check SC_P_Create
        assert 'SC_P_Create' in funcs
        assert funcs['SC_P_Create'] == {0: 's_SC_P_Create'}

        # Check SC_InitSide
        assert 'SC_InitSide' in funcs
        assert funcs['SC_InitSide'] == {1: 's_SC_initside'}

        # Check SC_InitSideGroup
        assert 'SC_InitSideGroup' in funcs
        assert funcs['SC_InitSideGroup'] == {0: 's_SC_initgroup'}

        # Check vector functions
        assert 'SC_P_GetPos' in funcs
        assert funcs['SC_P_GetPos'] == {1: 'c_Vector3'}

        assert 'SC_IsNear3D' in funcs
        assert funcs['SC_IsNear3D'] == {0: 'c_Vector3', 1: 'c_Vector3'}


class TestStructFieldOffsets:
    """Tests for correct field offset calculation."""

    def test_basic_offsets(self):
        """Test basic field offset calculation."""
        structs = get_struct_definitions()

        # c_Vector3: 3 floats at offsets 0, 4, 8
        assert 'c_Vector3' in structs
        fields = {f[1]: f[0] for f in structs['c_Vector3']}
        assert fields['x'] == 0
        assert fields['y'] == 4
        assert fields['z'] == 8

    def test_s_sphere_offsets(self):
        """Test s_sphere field offsets (contains c_Vector3)."""
        structs = get_struct_definitions()

        assert 's_sphere' in structs
        fields = {f[1]: f[0] for f in structs['s_sphere']}
        # pos is c_Vector3 at offset 0 (12 bytes)
        assert fields['pos'] == 0
        # rad is float at offset 12
        assert fields['rad'] == 12

    def test_s_SC_P_getinfo_offsets(self):
        """Test s_SC_P_getinfo field offsets."""
        structs = get_struct_definitions()

        assert 's_SC_P_getinfo' in structs
        fields = {f[1]: f[0] for f in structs['s_SC_P_getinfo']}
        assert fields['cur_hp'] == 0
        assert fields['max_hp'] == 4
        assert fields['side'] == 8
        assert fields['group'] == 12
        assert fields['member_id'] == 16

    def test_s_SC_initgroup_offsets(self):
        """Test s_SC_initgroup field offsets."""
        structs = get_struct_definitions()

        assert 's_SC_initgroup' in structs
        fields = {f[1]: f[0] for f in structs['s_SC_initgroup']}
        assert fields['SideId'] == 0
        assert fields['GroupId'] == 4
        assert fields['MaxPlayers'] == 8
        assert fields['NoHoldFireDistance'] == 12
        assert fields['follow_point_max_distance'] == 16


class TestIntegrationWithStructures:
    """Test integration with structures.py."""

    def test_infer_struct_from_function(self):
        """Test that infer_struct_from_function uses parsed data."""
        from vcdecomp.core.structures import infer_struct_from_function

        # Functions from parsed data
        assert infer_struct_from_function('SC_P_Create', 0) == 's_SC_P_Create'
        assert infer_struct_from_function('SC_InitSide', 1) == 's_SC_initside'
        assert infer_struct_from_function('SC_InitSideGroup', 0) == 's_SC_initgroup'
        assert infer_struct_from_function('SC_P_GetPos', 1) == 'c_Vector3'
        assert infer_struct_from_function('SC_SND_PlaySound3D', 1) == 'c_Vector3'

    def test_get_field_at_offset(self):
        """Test that get_field_at_offset uses parsed data."""
        from vcdecomp.core.structures import get_field_at_offset

        # Test c_Vector3 fields
        assert get_field_at_offset('c_Vector3', 0) == 'x'
        assert get_field_at_offset('c_Vector3', 4) == 'y'
        assert get_field_at_offset('c_Vector3', 8) == 'z'

        # Test s_SC_initside fields
        assert get_field_at_offset('s_SC_initside', 0) == 'MaxHideOutsStatus'
        assert get_field_at_offset('s_SC_initside', 4) == 'MaxGroups'

        # Test s_SC_initgroup fields
        assert get_field_at_offset('s_SC_initgroup', 0) == 'SideId'
        assert get_field_at_offset('s_SC_initgroup', 4) == 'GroupId'
        assert get_field_at_offset('s_SC_initgroup', 8) == 'MaxPlayers'

    def test_all_structures_populated(self):
        """Test that ALL_STRUCTURES includes parsed structures."""
        from vcdecomp.core.structures import ALL_STRUCTURES

        # Should have many structures
        assert len(ALL_STRUCTURES) >= 40

        # Check some parsed structs are present
        assert 's_SC_initside' in ALL_STRUCTURES
        assert 's_SC_initgroup' in ALL_STRUCTURES
        assert 's_SC_P_AI_props' in ALL_STRUCTURES
        assert 's_SC_MP_hud' in ALL_STRUCTURES
