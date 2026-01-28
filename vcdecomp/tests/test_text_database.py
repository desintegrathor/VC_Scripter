"""Tests for text_database module."""

import pytest
from vcdecomp.core.text_database import (
    parse_ingame_text,
    get_text_database,
    get_text,
    format_text_annotation,
    should_annotate_function,
    TEXT_ANNOTATION_FUNCTIONS,
    StructAssignmentTracker,
    StructTextIDs,
    TEXT_ID_MIN,
    TEXT_ID_MAX,
)


class TestParseIngameText:
    """Tests for parsing INGAME_TEXT.TXT file."""

    def test_loads_bundled_database(self):
        """Test that bundled database loads successfully."""
        db = get_text_database()
        # Should have loaded some entries
        assert len(db) > 100

    def test_get_text_existing(self):
        """Test getting existing text IDs."""
        # These are common game texts that should exist
        assert get_text(100) == "Not available in demo"
        assert get_text(101) == "Game inactive - waiting for both sides"
        assert get_text(102) == "US"
        assert get_text(103) == "VC"

    def test_get_text_missing(self):
        """Test getting missing text IDs returns None."""
        assert get_text(999999) is None
        assert get_text(-1) is None

    def test_format_annotation_single(self):
        """Test formatting single text ID."""
        annotation = format_text_annotation([100])
        assert annotation == '100: "Not available in demo"'

    def test_format_annotation_multiple(self):
        """Test formatting multiple text IDs."""
        annotation = format_text_annotation([102, 103])
        assert annotation == '102: "US" | 103: "VC"'

    def test_format_annotation_empty_for_missing(self):
        """Test that missing IDs return None."""
        annotation = format_text_annotation([999999])
        assert annotation is None

    def test_format_annotation_mixed(self):
        """Test mixed existing and missing IDs."""
        annotation = format_text_annotation([100, 999999, 101])
        # Should include only existing texts
        assert "100:" in annotation
        assert "101:" in annotation
        assert "999999" not in annotation

    def test_format_annotation_no_truncation_by_default(self):
        """Test that long texts are NOT truncated by default."""
        # Find a text with length > 50
        db = get_text_database()
        long_text_id = None
        long_text = None
        for tid, text in db.items():
            if len(text) > 50:
                long_text_id = tid
                long_text = text
                break

        if long_text_id:
            annotation = format_text_annotation([long_text_id])
            # Should NOT be truncated - full text should be present
            assert long_text in annotation
            assert not annotation.endswith("...")

    def test_format_annotation_truncates_with_max_length(self):
        """Test that texts are truncated when max_length is specified."""
        # Find a text with length > 50
        db = get_text_database()
        long_text_id = None
        for tid, text in db.items():
            if len(text) > 50:
                long_text_id = tid
                break

        if long_text_id:
            annotation = format_text_annotation([long_text_id], max_length=40)
            # Should be truncated with ...
            assert annotation.endswith("...")
            assert len(annotation) == 40


class TestShouldAnnotateFunction:
    """Tests for function annotation filtering."""

    def test_annotate_sc_wtxt(self):
        """SC_Wtxt should be annotated."""
        assert should_annotate_function("SC_Wtxt")

    def test_annotate_sc_gameinfo(self):
        """SC_GameInfo should be annotated."""
        assert should_annotate_function("SC_GameInfo")

    def test_annotate_sc_showmovieinfo(self):
        """SC_ShowMovieInfo should be annotated."""
        assert should_annotate_function("SC_ShowMovieInfo")

    def test_annotate_sc_missionsave(self):
        """SC_MissionSave should be annotated."""
        assert should_annotate_function("SC_MissionSave")

    def test_annotate_sc_setobjectives(self):
        """SC_SetObjectives should be annotated."""
        assert should_annotate_function("SC_SetObjectives")

    def test_annotate_speech_functions(self):
        """Speech/dialog functions should be annotated."""
        assert should_annotate_function("SC_SpeechRadio2")
        assert should_annotate_function("SC_P_Speech2")
        assert should_annotate_function("SC_P_SpeechMes2")
        assert should_annotate_function("SC_SpeechRadioMes2")
        assert should_annotate_function("SC_P_Speach")
        assert should_annotate_function("SC_P_SpeachMes")
        assert should_annotate_function("SC_P_SpeachRadio")
        assert should_annotate_function("SC_SpeachRadio")
        assert should_annotate_function("SC_SpeachRadioMes")

    def test_annotate_hud_functions(self):
        """HUD/UI functions should be annotated."""
        assert should_annotate_function("SC_SetCommandMenu")
        assert should_annotate_function("SC_ShowHelp")
        assert should_annotate_function("SC_ACTIVE_Add")
        assert should_annotate_function("SC_HUD_TextWriterInit")

    def test_no_annotate_other_functions(self):
        """Other functions should not be annotated."""
        assert not should_annotate_function("SC_P_Create")
        assert not should_annotate_function("SC_message")
        assert not should_annotate_function("SC_NOD_Get")


class TestStructAssignmentTracker:
    """Tests for struct assignment tracking."""

    def test_track_simple_assignment(self):
        """Test tracking simple constant assignment."""
        tracker = StructAssignmentTracker()
        tracker.track_assignment("local_80", 9136, 0)

        ids = tracker.get_text_ids_for_var("local_80")
        assert ids == [9136]

    def test_track_multiple_fields(self):
        """Test tracking assignments to multiple struct fields."""
        tracker = StructAssignmentTracker()
        tracker.track_assignment("local_80", 9136, 0)
        tracker.track_assignment("local_80", 9137, 1)

        ids = tracker.get_text_ids_for_var("local_80")
        # Should be sorted by field offset
        assert ids == [9136, 9137]

    def test_track_with_field_name(self):
        """Test tracking assignment with field name in target."""
        tracker = StructAssignmentTracker()
        tracker.track_assignment("local_80.field0", 9136)
        tracker.track_assignment("local_80.field1", 9137)

        ids = tracker.get_text_ids_for_var("local_80")
        assert ids == [9136, 9137]

    def test_get_with_address_prefix(self):
        """Test getting IDs with & prefix in variable name."""
        tracker = StructAssignmentTracker()
        tracker.track_assignment("local_80", 9136, 0)

        # Should work with or without & prefix
        ids = tracker.get_text_ids_for_var("&local_80")
        assert ids == [9136]

    def test_skip_values_outside_range(self):
        """Test that values outside text ID range are not tracked."""
        tracker = StructAssignmentTracker()
        tracker.track_assignment("local_80", 50, 0)  # Too low
        tracker.track_assignment("local_80", 200000, 1)  # Too high

        ids = tracker.get_text_ids_for_var("local_80")
        assert ids == []

    def test_ignore_non_local_variables(self):
        """Test that non-local variables are not tracked."""
        tracker = StructAssignmentTracker()
        tracker.track_assignment("global_0", 9136, 0)
        tracker.track_assignment("data_100", 9137, 0)

        assert tracker.get_text_ids_for_var("global_0") == []
        assert tracker.get_text_ids_for_var("data_100") == []

    def test_get_struct_text_ids(self):
        """Test getting structured information."""
        tracker = StructAssignmentTracker()
        tracker.track_assignment("local_80", 9136, 0)
        tracker.track_assignment("local_80", 9137, 4)

        result = tracker.get_struct_text_ids("local_80")
        assert result is not None
        assert result.var_name == "local_80"
        assert result.text_ids == [9136, 9137]
        assert result.field_offsets == [0, 4]

    def test_get_struct_text_ids_missing(self):
        """Test getting structured info for missing variable."""
        tracker = StructAssignmentTracker()
        result = tracker.get_struct_text_ids("local_999")
        assert result is None

    def test_clear_all(self):
        """Test clearing all tracked assignments."""
        tracker = StructAssignmentTracker()
        tracker.track_assignment("local_80", 9136, 0)
        tracker.track_assignment("local_90", 9137, 0)

        tracker.clear()

        assert tracker.get_text_ids_for_var("local_80") == []
        assert tracker.get_text_ids_for_var("local_90") == []

    def test_clear_specific_var(self):
        """Test clearing assignments for specific variable."""
        tracker = StructAssignmentTracker()
        tracker.track_assignment("local_80", 9136, 0)
        tracker.track_assignment("local_90", 9137, 0)

        tracker.clear_var("local_80")

        assert tracker.get_text_ids_for_var("local_80") == []
        assert tracker.get_text_ids_for_var("local_90") == [9137]

    def test_multiple_variables(self):
        """Test tracking multiple different variables."""
        tracker = StructAssignmentTracker()
        tracker.track_assignment("local_80", 9136, 0)
        tracker.track_assignment("local_80", 9137, 1)
        tracker.track_assignment("local_100", 9200, 0)
        tracker.track_assignment("local_100", 9201, 1)

        assert tracker.get_text_ids_for_var("local_80") == [9136, 9137]
        assert tracker.get_text_ids_for_var("local_100") == [9200, 9201]

    def test_known_field_names(self):
        """Test parsing known struct field names."""
        tracker = StructAssignmentTracker()
        tracker.track_assignment("local_80.savename_id", 9136)
        tracker.track_assignment("local_80.description_id", 9137)

        ids = tracker.get_text_ids_for_var("local_80")
        # savename_id maps to offset 0, description_id to offset 1
        assert ids == [9136, 9137]

    def test_array_indexed_assignment(self):
        """Test tracking assignments with array indexing like local_63[0].y"""
        tracker = StructAssignmentTracker()
        tracker.track_assignment("local_63[0].y", 3490)
        tracker.track_assignment("local_63[0].z", 3491)

        ids = tracker.get_text_ids_for_var("local_63")
        # y maps to offset 1, z to offset 2
        assert ids == [3490, 3491]

    def test_array_indexed_with_x_y_z_w(self):
        """Test vector fields x, y, z, w mapping to offsets 0, 1, 2, 3."""
        tracker = StructAssignmentTracker()
        tracker.track_assignment("local_10[0].x", 1000)
        tracker.track_assignment("local_10[0].y", 1001)
        tracker.track_assignment("local_10[0].z", 1002)
        tracker.track_assignment("local_10[0].w", 1003)

        ids = tracker.get_text_ids_for_var("local_10")
        assert ids == [1000, 1001, 1002, 1003]
