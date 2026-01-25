"""
Tests for the cover (live range) module.
"""

import pytest

from vcdecomp.core.ir.merge.cover import Cover, CoverPiece, compute_cover


class TestCoverPiece:
    """Test CoverPiece data structure."""

    def test_creation(self):
        """Test creating a cover piece."""
        piece = CoverPiece(block_id=1, start_addr=100, end_addr=200)
        assert piece.block_id == 1
        assert piece.start_addr == 100
        assert piece.end_addr == 200

    def test_contains_point_inside(self):
        """Test point inside cover piece."""
        piece = CoverPiece(block_id=1, start_addr=100, end_addr=200)
        assert piece.contains(1, 150)

    def test_contains_point_at_start(self):
        """Test point at start of cover piece."""
        piece = CoverPiece(block_id=1, start_addr=100, end_addr=200)
        assert piece.contains(1, 100)

    def test_contains_point_at_end(self):
        """Test point at end of cover piece."""
        piece = CoverPiece(block_id=1, start_addr=100, end_addr=200)
        assert piece.contains(1, 200)

    def test_contains_point_wrong_block(self):
        """Test point in wrong block."""
        piece = CoverPiece(block_id=1, start_addr=100, end_addr=200)
        assert not piece.contains(2, 150)

    def test_contains_point_before(self):
        """Test point before cover piece."""
        piece = CoverPiece(block_id=1, start_addr=100, end_addr=200)
        assert not piece.contains(1, 50)

    def test_contains_point_after(self):
        """Test point after cover piece."""
        piece = CoverPiece(block_id=1, start_addr=100, end_addr=200)
        assert not piece.contains(1, 250)

    def test_overlaps_same_block_overlap(self):
        """Test overlap detection with actual overlap."""
        piece1 = CoverPiece(block_id=1, start_addr=100, end_addr=200)
        piece2 = CoverPiece(block_id=1, start_addr=150, end_addr=250)
        assert piece1.overlaps(piece2)
        assert piece2.overlaps(piece1)

    def test_overlaps_same_block_no_overlap(self):
        """Test no overlap without overlap."""
        piece1 = CoverPiece(block_id=1, start_addr=100, end_addr=200)
        piece2 = CoverPiece(block_id=1, start_addr=300, end_addr=400)
        assert not piece1.overlaps(piece2)
        assert not piece2.overlaps(piece1)

    def test_overlaps_different_blocks(self):
        """Test no overlap in different blocks."""
        piece1 = CoverPiece(block_id=1, start_addr=100, end_addr=200)
        piece2 = CoverPiece(block_id=2, start_addr=100, end_addr=200)
        assert not piece1.overlaps(piece2)

    def test_overlaps_adjacent(self):
        """Test adjacent pieces (touching at boundary)."""
        piece1 = CoverPiece(block_id=1, start_addr=100, end_addr=200)
        piece2 = CoverPiece(block_id=1, start_addr=201, end_addr=300)
        # Adjacent pieces should NOT overlap (they touch but don't share points)
        assert not piece1.overlaps(piece2)

    def test_adjacent_pieces(self):
        """Test adjacent detection."""
        piece1 = CoverPiece(block_id=1, start_addr=100, end_addr=200)
        piece2 = CoverPiece(block_id=1, start_addr=201, end_addr=300)
        assert piece1.adjacent(piece2)

    def test_merge_overlapping(self):
        """Test merging overlapping pieces."""
        piece1 = CoverPiece(block_id=1, start_addr=100, end_addr=200)
        piece2 = CoverPiece(block_id=1, start_addr=150, end_addr=250)
        merged = piece1.merge(piece2)
        assert merged is not None
        assert merged.start_addr == 100
        assert merged.end_addr == 250

    def test_merge_adjacent(self):
        """Test merging adjacent pieces."""
        piece1 = CoverPiece(block_id=1, start_addr=100, end_addr=200)
        piece2 = CoverPiece(block_id=1, start_addr=201, end_addr=300)
        merged = piece1.merge(piece2)
        assert merged is not None
        assert merged.start_addr == 100
        assert merged.end_addr == 300

    def test_merge_different_blocks(self):
        """Test merging fails for different blocks."""
        piece1 = CoverPiece(block_id=1, start_addr=100, end_addr=200)
        piece2 = CoverPiece(block_id=2, start_addr=150, end_addr=250)
        merged = piece1.merge(piece2)
        assert merged is None


class TestCover:
    """Test Cover class."""

    def test_empty_cover(self):
        """Test empty cover."""
        cover = Cover()
        assert len(cover.pieces) == 0
        assert cover.is_empty()

    def test_add_def_point(self):
        """Test adding definition point."""
        cover = Cover()
        cover.add_def_point(block_id=1, addr=100)
        assert len(cover.pieces) == 1
        assert cover.pieces[0].block_id == 1
        assert cover.pieces[0].start_addr == 100

    def test_add_use_point_extends(self):
        """Test that use point extends cover."""
        cover = Cover()
        cover.add_def_point(block_id=1, addr=100)
        cover.add_use_point(block_id=1, addr=200)
        assert len(cover.pieces) == 1
        assert cover.pieces[0].end_addr == 200

    def test_add_use_point_different_block(self):
        """Test use point in different block creates new piece."""
        cover = Cover()
        cover.add_def_point(block_id=1, addr=100)
        cover.add_use_point(block_id=2, addr=150)
        assert len(cover.pieces) == 2

    def test_intersects_with_overlap(self):
        """Test cover intersection with overlap."""
        cover1 = Cover()
        cover1.add_def_point(1, 100)
        cover1.add_use_point(1, 200)

        cover2 = Cover()
        cover2.add_def_point(1, 150)
        cover2.add_use_point(1, 250)

        assert cover1.intersects(cover2)
        assert cover2.intersects(cover1)

    def test_intersects_no_overlap(self):
        """Test cover intersection without overlap."""
        cover1 = Cover()
        cover1.add_def_point(1, 100)
        cover1.add_use_point(1, 200)

        cover2 = Cover()
        cover2.add_def_point(1, 300)
        cover2.add_use_point(1, 400)

        assert not cover1.intersects(cover2)
        assert not cover2.intersects(cover1)

    def test_intersects_different_blocks(self):
        """Test cover intersection in different blocks."""
        cover1 = Cover()
        cover1.add_def_point(1, 100)
        cover1.add_use_point(1, 200)

        cover2 = Cover()
        cover2.add_def_point(2, 100)
        cover2.add_use_point(2, 200)

        assert not cover1.intersects(cover2)

    def test_merge_covers(self):
        """Test merging two covers."""
        cover1 = Cover()
        cover1.add_def_point(1, 100)
        cover1.add_use_point(1, 200)

        cover2 = Cover()
        cover2.add_def_point(2, 150)
        cover2.add_use_point(2, 250)

        cover1.merge(cover2)
        assert len(cover1.pieces) == 2

    def test_contains_point(self):
        """Test checking if cover contains point."""
        cover = Cover()
        cover.add_def_point(1, 100)
        cover.add_use_point(1, 200)

        assert cover.contains(1, 150)
        assert not cover.contains(1, 50)
        assert not cover.contains(2, 150)

    def test_multiple_pieces_same_block(self):
        """Test multiple non-contiguous pieces in same block."""
        cover = Cover()
        cover.add_def_point(1, 100)
        cover.add_use_point(1, 150)
        # Gap
        cover.add_def_point(1, 300)
        cover.add_use_point(1, 350)

        assert len(cover.pieces) >= 1  # May merge or keep separate

    def test_get_block_ids(self):
        """Test getting block IDs from cover."""
        cover = Cover()
        cover.add_def_point(1, 100)
        cover.add_def_point(2, 200)
        cover.add_def_point(3, 300)

        block_ids = cover.get_block_ids()
        assert block_ids == {1, 2, 3}

    def test_add_range(self):
        """Test adding a range directly."""
        cover = Cover()
        cover.add_range(1, 100, 200)
        assert len(cover.pieces) == 1
        assert cover.pieces[0].start_addr == 100
        assert cover.pieces[0].end_addr == 200


class TestComputeCover:
    """Test compute_cover function."""

    def test_compute_cover_no_function(self):
        """Test compute_cover with no SSA function."""
        # Create a mock value
        class MockValue:
            name = "test_v1"

        cover = compute_cover(MockValue(), None)
        assert isinstance(cover, Cover)

    def test_compute_cover_mock_value(self):
        """Test compute_cover with mock value and function."""
        class MockValue:
            name = "test_v1"
            def_block = 1
            def_addr = 100
            uses = []

        class MockSSAFunc:
            pass

        cover = compute_cover(MockValue(), MockSSAFunc())
        assert isinstance(cover, Cover)
        assert len(cover.pieces) == 1

    def test_compute_cover_with_uses(self):
        """Test compute_cover with uses that have block_id and addr."""
        class MockUse:
            def __init__(self, block_id, addr):
                self.block_id = block_id
                self.addr = addr

        class MockValue:
            name = "test_v1"
            def_block = 1
            def_addr = 100
            uses = [MockUse(1, 150), MockUse(1, 200)]

        class MockSSAFunc:
            pass

        cover = compute_cover(MockValue(), MockSSAFunc())
        assert isinstance(cover, Cover)
        # Should have definition extended by uses
        assert cover.contains(1, 150)
        assert cover.contains(1, 200)

