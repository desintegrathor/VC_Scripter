"""
Report generator for validation results.

Generates human-readable reports from ValidationResult in multiple formats:
- Text format with color coding (ANSI)
- HTML format with expandable sections
- JSON format for programmatic use
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, List
from datetime import datetime
import json
import html

from .validation_types import ValidationResult, ValidationVerdict
from .difference_types import CategorizedDifference, DifferenceCategory, DifferenceSummary
from .bytecode_compare import DifferenceSeverity


class ANSIColors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"

    # Verdict colors
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"

    # Severity colors
    INFO = "\033[36m"      # Cyan
    MINOR = "\033[33m"     # Yellow
    MAJOR = "\033[33m"     # Yellow
    CRITICAL = "\033[31m"  # Red

    # Category colors
    SEMANTIC = "\033[35m"      # Magenta
    COSMETIC = "\033[36m"      # Cyan
    OPTIMIZATION = "\033[34m"  # Blue
    UNKNOWN = "\033[37m"       # Gray


class ReportGenerator:
    """
    Generates validation reports in multiple formats.

    Supports text (with ANSI colors), HTML (with expandable sections),
    and JSON (for programmatic use) output formats.
    """

    def __init__(self, use_colors: bool = True):
        """
        Initialize report generator.

        Args:
            use_colors: Whether to use ANSI colors in text output
        """
        self.use_colors = use_colors

    def generate_text_report(self, result: ValidationResult) -> str:
        """
        Generate a text report with optional ANSI color coding.

        Args:
            result: Validation result to report on

        Returns:
            Formatted text report
        """
        lines = []

        # Header
        lines.append(self._colorize("=" * 80, ANSIColors.BOLD))
        lines.append(self._colorize("VALIDATION REPORT", ANSIColors.BOLD))
        lines.append(self._colorize("=" * 80, ANSIColors.BOLD))
        lines.append("")

        # Timestamp
        if "timestamp" in result.metadata:
            lines.append(f"Generated: {result.metadata['timestamp']}")
        else:
            lines.append(f"Generated: {datetime.now().isoformat()}")
        lines.append("")

        # Verdict section
        lines.extend(self._format_verdict_section(result))
        lines.append("")

        # Files section
        lines.append(self._colorize("FILES", ANSIColors.BOLD))
        lines.append("-" * 80)
        lines.append(f"Original .SCR:     {result.original_scr}")
        lines.append(f"Decompiled Source: {result.decompiled_source}")
        if result.compilation_result and result.compilation_result.output_file:
            lines.append(f"Recompiled .SCR:   {result.compilation_result.output_file}")
        lines.append("")

        # Compilation section
        lines.extend(self._format_compilation_section(result))
        lines.append("")

        # Comparison section
        if result.comparison_succeeded:
            lines.extend(self._format_comparison_section(result))
            lines.append("")

        # Differences section (detailed)
        if result.categorized_differences:
            lines.extend(self._format_differences_section(result))
            lines.append("")

        # Recommendations section
        if result.recommendations:
            lines.extend(self._format_recommendations_section(result))
            lines.append("")

        # Footer
        lines.append(self._colorize("=" * 80, ANSIColors.BOLD))

        return "\n".join(lines)

    def generate_html_report(self, result: ValidationResult) -> str:
        """
        Generate an HTML report with expandable sections.

        Args:
            result: Validation result to report on

        Returns:
            Formatted HTML report
        """
        timestamp = result.metadata.get("timestamp", datetime.now().isoformat())

        # Build HTML sections
        verdict_html = self._format_verdict_html(result)
        files_html = self._format_files_html(result)
        compilation_html = self._format_compilation_html(result)
        comparison_html = self._format_comparison_html(result)
        differences_html = self._format_differences_html(result)
        recommendations_html = self._format_recommendations_html(result)

        # Build complete HTML document
        html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Validation Report - {html.escape(str(result.original_scr.name))}</title>
    <style>
        {self._get_html_styles()}
    </style>
    <script>
        {self._get_html_scripts()}
    </script>
</head>
<body>
    <div class="container">
        <header>
            <h1>Validation Report</h1>
            <p class="timestamp">Generated: {html.escape(timestamp)}</p>
        </header>

        {verdict_html}
        {files_html}
        {compilation_html}
        {comparison_html}
        {differences_html}
        {recommendations_html}

        <footer>
            <p>Generated by VC Script Decompiler Validation System</p>
        </footer>
    </div>
</body>
</html>
"""
        return html_doc

    def generate_json_report(self, result: ValidationResult, indent: int = 2) -> str:
        """
        Generate a JSON report for programmatic use.

        Args:
            result: Validation result to report on
            indent: JSON indentation level

        Returns:
            JSON string
        """
        # Use the existing to_dict method and enhance with additional report metadata
        report_data = result.to_dict()

        # Add report metadata
        report_data["report_metadata"] = {
            "format_version": "1.0",
            "generated_at": result.metadata.get("timestamp", datetime.now().isoformat()),
            "generator": "VC Script Decompiler Validation System",
        }

        # Add detailed differences if available
        if result.categorized_differences:
            report_data["differences"] = [
                {
                    "type": diff.difference.type.value,
                    "severity": diff.difference.severity.value,
                    "category": diff.category.value,
                    "location": diff.difference.location,
                    "description": diff.difference.description,
                    "original_value": str(diff.difference.original_value) if diff.difference.original_value is not None else None,
                    "recompiled_value": str(diff.difference.recompiled_value) if diff.difference.recompiled_value is not None else None,
                    "details": diff.difference.details,
                    "rationale": diff.rationale,
                }
                for diff in result.categorized_differences
            ]

        return json.dumps(report_data, indent=indent)

    def save_report(
        self,
        result: ValidationResult,
        output_path: Path,
        format: str = "auto"
    ) -> None:
        """
        Save report to a file.

        Args:
            result: Validation result to report on
            output_path: Path to save the report to
            format: Report format ('text', 'html', 'json', or 'auto' to detect from extension)
        """
        output_path = Path(output_path)

        # Auto-detect format from extension
        if format == "auto":
            ext = output_path.suffix.lower()
            if ext == ".html":
                format = "html"
            elif ext == ".json":
                format = "json"
            else:
                format = "text"

        # Generate report content
        if format == "html":
            content = self.generate_html_report(result)
        elif format == "json":
            content = self.generate_json_report(result)
        else:
            content = self.generate_text_report(result)

        # Write to file
        output_path.write_text(content, encoding="utf-8")

    # ========================================================================
    # Text format helpers
    # ========================================================================

    def _colorize(self, text: str, color: str) -> str:
        """Apply ANSI color to text if colors are enabled."""
        if not self.use_colors:
            return text
        return f"{color}{text}{ANSIColors.RESET}"

    def _format_verdict_section(self, result: ValidationResult) -> List[str]:
        """Format the verdict section for text output."""
        lines = []
        lines.append(self._colorize("VERDICT", ANSIColors.BOLD))
        lines.append("-" * 80)

        # Verdict with color
        verdict_color = {
            ValidationVerdict.PASS: ANSIColors.GREEN,
            ValidationVerdict.PARTIAL: ANSIColors.YELLOW,
            ValidationVerdict.FAIL: ANSIColors.RED,
            ValidationVerdict.ERROR: ANSIColors.RED,
        }
        verdict_symbol = {
            ValidationVerdict.PASS: "✓",
            ValidationVerdict.PARTIAL: "⚠",
            ValidationVerdict.FAIL: "✗",
            ValidationVerdict.ERROR: "✗",
        }

        color = verdict_color.get(result.verdict, ANSIColors.RESET)
        symbol = verdict_symbol.get(result.verdict, "•")
        verdict_text = f"{symbol} {result.verdict.value.upper()}"
        lines.append(self._colorize(verdict_text, color + ANSIColors.BOLD))

        # Error message if present
        if result.error_message:
            lines.append(f"\nError: {result.error_message}")

        return lines

    def _format_compilation_section(self, result: ValidationResult) -> List[str]:
        """Format the compilation section for text output."""
        lines = []
        lines.append(self._colorize("COMPILATION", ANSIColors.BOLD))
        lines.append("-" * 80)

        if not result.compilation_result:
            lines.append("⚠ No compilation result available")
            return lines

        comp = result.compilation_result

        if comp.success:
            lines.append(self._colorize("✓ Compilation succeeded", ANSIColors.GREEN))
            if comp.output_file:
                lines.append(f"  Output: {comp.output_file}")
            if comp.has_warnings:
                lines.append(self._colorize(f"  Warnings: {comp.warning_count}", ANSIColors.YELLOW))
        else:
            lines.append(self._colorize("✗ Compilation failed", ANSIColors.RED))
            if comp.has_errors:
                lines.append(f"  Errors: {comp.error_count}")
                lines.append("\n  First few errors:")
                for err in comp.errors[:5]:
                    lines.append(f"    {err}")
                if len(comp.errors) > 5:
                    lines.append(f"    ... and {len(comp.errors) - 5} more")

        return lines

    def _format_comparison_section(self, result: ValidationResult) -> List[str]:
        """Format the comparison section for text output."""
        lines = []
        lines.append(self._colorize("BYTECODE COMPARISON", ANSIColors.BOLD))
        lines.append("-" * 80)

        if result.bytecode_identical:
            lines.append(self._colorize("✓ Bytecode is identical!", ANSIColors.GREEN + ANSIColors.BOLD))
            return lines

        if not result.difference_summary:
            lines.append("⚠ No comparison summary available")
            return lines

        summary = result.difference_summary
        lines.append(f"Found {summary.total_count} differences\n")

        # By category
        lines.append(self._colorize("By Category:", ANSIColors.BOLD))
        category_data = [
            ("Semantic", summary.semantic_count, ANSIColors.SEMANTIC),
            ("Cosmetic", summary.cosmetic_count, ANSIColors.COSMETIC),
            ("Optimization", summary.optimization_count, ANSIColors.OPTIMIZATION),
            ("Unknown", summary.unknown_count, ANSIColors.UNKNOWN),
        ]
        for name, count, color in category_data:
            if count > 0:
                lines.append(f"  {self._colorize(name, color)}: {count}")

        # By severity
        lines.append(f"\n{self._colorize('By Severity:', ANSIColors.BOLD)}")
        severity_data = [
            ("Critical", summary.critical_count, ANSIColors.CRITICAL),
            ("Major", summary.major_count, ANSIColors.MAJOR),
            ("Minor", summary.minor_count, ANSIColors.MINOR),
            ("Info", summary.info_count, ANSIColors.INFO),
        ]
        for name, count, color in severity_data:
            if count > 0:
                lines.append(f"  {self._colorize(name, color)}: {count}")

        return lines

    def _format_differences_section(self, result: ValidationResult) -> List[str]:
        """Format the detailed differences section for text output."""
        lines = []
        lines.append(self._colorize("DETAILED DIFFERENCES", ANSIColors.BOLD))
        lines.append("-" * 80)

        if not result.categorized_differences:
            lines.append("No differences found")
            return lines

        # Group by category
        categories = [
            (DifferenceCategory.SEMANTIC, "SEMANTIC DIFFERENCES (affect behavior)", ANSIColors.SEMANTIC),
            (DifferenceCategory.COSMETIC, "COSMETIC DIFFERENCES (no behavioral impact)", ANSIColors.COSMETIC),
            (DifferenceCategory.OPTIMIZATION, "OPTIMIZATION DIFFERENCES (equivalent implementation)", ANSIColors.OPTIMIZATION),
            (DifferenceCategory.UNKNOWN, "UNKNOWN DIFFERENCES (unclear impact)", ANSIColors.UNKNOWN),
        ]

        for category, title, color in categories:
            diffs = [d for d in result.categorized_differences if d.category == category]
            if not diffs:
                continue

            lines.append("")
            lines.append(self._colorize(f"{title} ({len(diffs)})", color + ANSIColors.BOLD))
            lines.append("")

            for diff in diffs[:10]:  # Show first 10 per category
                severity_symbol = {
                    DifferenceSeverity.INFO: "ℹ",
                    DifferenceSeverity.MINOR: "⚠",
                    DifferenceSeverity.MAJOR: "⚠",
                    DifferenceSeverity.CRITICAL: "✗",
                }
                symbol = severity_symbol.get(diff.difference.severity, "•")

                lines.append(f"  {symbol} [{diff.difference.type.value}] {diff.difference.location}")
                lines.append(f"      {diff.difference.description}")
                if diff.difference.original_value is not None and diff.difference.recompiled_value is not None:
                    lines.append(f"      Original:    {diff.difference.original_value}")
                    lines.append(f"      Recompiled:  {diff.difference.recompiled_value}")
                lines.append("")

            if len(diffs) > 10:
                lines.append(f"  ... and {len(diffs) - 10} more {category.value} differences")
                lines.append("")

        return lines

    def _format_recommendations_section(self, result: ValidationResult) -> List[str]:
        """Format the recommendations section for text output."""
        lines = []
        lines.append(self._colorize("RECOMMENDATIONS", ANSIColors.BOLD))
        lines.append("-" * 80)

        if not result.recommendations:
            lines.append("No recommendations available")
            return lines

        for i, rec in enumerate(result.recommendations, 1):
            lines.append(f"{i}. {rec}")

        return lines

    # ========================================================================
    # HTML format helpers
    # ========================================================================

    def _get_html_styles(self) -> str:
        """Get CSS styles for HTML report."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        header h1 {
            font-size: 2em;
            margin-bottom: 10px;
        }

        .timestamp {
            opacity: 0.9;
            font-size: 0.9em;
        }

        .section {
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .section h2 {
            font-size: 1.5em;
            margin-bottom: 15px;
            color: #667eea;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 10px;
        }

        .verdict {
            font-size: 2em;
            font-weight: bold;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            margin: 10px 0;
        }

        .verdict.pass { background: #d4edda; color: #155724; }
        .verdict.partial { background: #fff3cd; color: #856404; }
        .verdict.fail { background: #f8d7da; color: #721c24; }
        .verdict.error { background: #f8d7da; color: #721c24; }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }

        .stat-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #667eea;
        }

        .stat-card h3 {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }

        .stat-card .value {
            font-size: 1.8em;
            font-weight: bold;
            color: #333;
        }

        .stat-card.semantic { border-left-color: #dc3545; }
        .stat-card.cosmetic { border-left-color: #17a2b8; }
        .stat-card.optimization { border-left-color: #007bff; }
        .stat-card.critical { border-left-color: #dc3545; }
        .stat-card.major { border-left-color: #ffc107; }
        .stat-card.minor { border-left-color: #28a745; }

        .expandable {
            margin: 10px 0;
        }

        .expandable summary {
            cursor: pointer;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 4px;
            font-weight: bold;
            user-select: none;
        }

        .expandable summary:hover {
            background: #e9ecef;
        }

        .expandable-content {
            padding: 15px;
            border-left: 3px solid #e0e0e0;
            margin-left: 10px;
        }

        .difference {
            background: #f8f9fa;
            padding: 12px;
            margin: 8px 0;
            border-radius: 4px;
            border-left: 4px solid #6c757d;
        }

        .difference.critical { border-left-color: #dc3545; }
        .difference.major { border-left-color: #ffc107; }
        .difference.minor { border-left-color: #28a745; }
        .difference.info { border-left-color: #17a2b8; }

        .difference-header {
            font-weight: bold;
            margin-bottom: 5px;
        }

        .difference-location {
            color: #666;
            font-size: 0.9em;
            font-family: 'Courier New', monospace;
        }

        .difference-values {
            margin-top: 8px;
            font-size: 0.9em;
            font-family: 'Courier New', monospace;
        }

        .recommendation {
            padding: 10px;
            margin: 8px 0;
            background: #e7f3ff;
            border-left: 4px solid #007bff;
            border-radius: 4px;
        }

        footer {
            text-align: center;
            color: #666;
            padding: 20px;
            font-size: 0.9em;
        }

        .file-list {
            list-style: none;
            padding: 0;
        }

        .file-list li {
            padding: 8px;
            margin: 5px 0;
            background: #f8f9fa;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }

        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 4px;
            border-left: 4px solid #dc3545;
        }
        """

    def _get_html_scripts(self) -> str:
        """Get JavaScript for HTML report interactivity."""
        return """
        document.addEventListener('DOMContentLoaded', function() {
            // Add click handlers for expandable sections
            const details = document.querySelectorAll('details');
            details.forEach(detail => {
                detail.addEventListener('toggle', function() {
                    if (this.open) {
                        this.querySelector('summary').textContent =
                            this.querySelector('summary').textContent.replace('▶', '▼');
                    } else {
                        this.querySelector('summary').textContent =
                            this.querySelector('summary').textContent.replace('▼', '▶');
                    }
                });
            });
        });
        """

    def _format_verdict_html(self, result: ValidationResult) -> str:
        """Format verdict section for HTML."""
        verdict_class = result.verdict.value
        symbol = {"pass": "✓", "partial": "⚠", "fail": "✗", "error": "✗"}.get(result.verdict.value, "•")

        error_html = ""
        if result.error_message:
            error_html = f'<div class="error-message">{html.escape(result.error_message)}</div>'

        return f"""
        <section class="section">
            <h2>Verdict</h2>
            <div class="verdict {verdict_class}">
                {symbol} {result.verdict.value.upper()}
            </div>
            {error_html}
        </section>
        """

    def _format_files_html(self, result: ValidationResult) -> str:
        """Format files section for HTML."""
        recompiled_html = ""
        if result.compilation_result and result.compilation_result.output_file:
            recompiled_html = f"<li><strong>Recompiled .SCR:</strong> {html.escape(str(result.compilation_result.output_file))}</li>"

        return f"""
        <section class="section">
            <h2>Files</h2>
            <ul class="file-list">
                <li><strong>Original .SCR:</strong> {html.escape(str(result.original_scr))}</li>
                <li><strong>Decompiled Source:</strong> {html.escape(str(result.decompiled_source))}</li>
                {recompiled_html}
            </ul>
        </section>
        """

    def _format_compilation_html(self, result: ValidationResult) -> str:
        """Format compilation section for HTML."""
        if not result.compilation_result:
            return """
            <section class="section">
                <h2>Compilation</h2>
                <p>⚠ No compilation result available</p>
            </section>
            """

        comp = result.compilation_result

        if comp.success:
            warnings_html = ""
            if comp.has_warnings:
                warnings_html = f"<p>⚠ Warnings: {comp.warning_count}</p>"

            return f"""
            <section class="section">
                <h2>Compilation</h2>
                <p style="color: green; font-weight: bold;">✓ Compilation succeeded</p>
                {warnings_html}
            </section>
            """
        else:
            errors_html = ""
            if comp.errors:
                error_items = "".join(
                    f"<li>{html.escape(str(err))}</li>"
                    for err in comp.errors[:10]
                )
                if len(comp.errors) > 10:
                    error_items += f"<li>... and {len(comp.errors) - 10} more</li>"
                errors_html = f"<ul>{error_items}</ul>"

            return f"""
            <section class="section">
                <h2>Compilation</h2>
                <p style="color: red; font-weight: bold;">✗ Compilation failed</p>
                <p>Errors: {comp.error_count}</p>
                {errors_html}
            </section>
            """

    def _format_comparison_html(self, result: ValidationResult) -> str:
        """Format comparison section for HTML."""
        if not result.comparison_succeeded:
            return ""

        if result.bytecode_identical:
            return """
            <section class="section">
                <h2>Bytecode Comparison</h2>
                <p style="color: green; font-weight: bold; font-size: 1.2em;">✓ Bytecode is identical!</p>
            </section>
            """

        if not result.difference_summary:
            return ""

        summary = result.difference_summary

        # Build stats cards
        category_cards = ""
        for name, count, css_class in [
            ("Semantic", summary.semantic_count, "semantic"),
            ("Cosmetic", summary.cosmetic_count, "cosmetic"),
            ("Optimization", summary.optimization_count, "optimization"),
        ]:
            if count > 0:
                category_cards += f"""
                <div class="stat-card {css_class}">
                    <h3>{name}</h3>
                    <div class="value">{count}</div>
                </div>
                """

        severity_cards = ""
        for name, count, css_class in [
            ("Critical", summary.critical_count, "critical"),
            ("Major", summary.major_count, "major"),
            ("Minor", summary.minor_count, "minor"),
        ]:
            if count > 0:
                severity_cards += f"""
                <div class="stat-card {css_class}">
                    <h3>{name}</h3>
                    <div class="value">{count}</div>
                </div>
                """

        return f"""
        <section class="section">
            <h2>Bytecode Comparison</h2>
            <p style="font-size: 1.2em; font-weight: bold;">Found {summary.total_count} differences</p>

            <h3 style="margin-top: 20px;">By Category</h3>
            <div class="stats">
                {category_cards}
            </div>

            <h3 style="margin-top: 20px;">By Severity</h3>
            <div class="stats">
                {severity_cards}
            </div>
        </section>
        """

    def _format_differences_html(self, result: ValidationResult) -> str:
        """Format detailed differences section for HTML."""
        if not result.categorized_differences:
            return ""

        sections_html = ""

        # Group by category
        for category, title in [
            (DifferenceCategory.SEMANTIC, "Semantic Differences (affect behavior)"),
            (DifferenceCategory.COSMETIC, "Cosmetic Differences (no behavioral impact)"),
            (DifferenceCategory.OPTIMIZATION, "Optimization Differences (equivalent implementation)"),
            (DifferenceCategory.UNKNOWN, "Unknown Differences (unclear impact)"),
        ]:
            diffs = [d for d in result.categorized_differences if d.category == category]
            if not diffs:
                continue

            diffs_html = ""
            for diff in diffs[:20]:  # Show first 20 per category
                severity_class = diff.difference.severity.value

                values_html = ""
                if diff.difference.original_value is not None and diff.difference.recompiled_value is not None:
                    values_html = f"""
                    <div class="difference-values">
                        <div>Original: {html.escape(str(diff.difference.original_value))}</div>
                        <div>Recompiled: {html.escape(str(diff.difference.recompiled_value))}</div>
                    </div>
                    """

                diffs_html += f"""
                <div class="difference {severity_class}">
                    <div class="difference-header">{html.escape(diff.difference.description)}</div>
                    <div class="difference-location">[{diff.difference.type.value}] {html.escape(diff.difference.location)}</div>
                    {values_html}
                </div>
                """

            if len(diffs) > 20:
                diffs_html += f"<p><em>... and {len(diffs) - 20} more {category.value} differences</em></p>"

            sections_html += f"""
            <details class="expandable" open>
                <summary>▼ {title} ({len(diffs)})</summary>
                <div class="expandable-content">
                    {diffs_html}
                </div>
            </details>
            """

        return f"""
        <section class="section">
            <h2>Detailed Differences</h2>
            {sections_html}
        </section>
        """

    def _format_recommendations_html(self, result: ValidationResult) -> str:
        """Format recommendations section for HTML."""
        if not result.recommendations:
            return ""

        recs_html = "".join(
            f'<div class="recommendation">{html.escape(rec)}</div>'
            for rec in result.recommendations
        )

        return f"""
        <section class="section">
            <h2>Recommendations</h2>
            {recs_html}
        </section>
        """
