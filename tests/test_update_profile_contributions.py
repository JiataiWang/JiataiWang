from __future__ import annotations

import re
import sys
import unittest
import xml.etree.ElementTree as ElementTree
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from update_profile_contributions import (  # noqa: E402
    CHINESE_HEADER,
    CHINESE_HEADING,
    CHINESE_SEPARATOR,
    ENGLISH_HEADER,
    ENGLISH_HEADING,
    ENGLISH_SEPARATOR,
    PullRequest,
    STAR_BADGE_HEIGHT,
    STAR_BADGE_WIDTH,
    _format_star_count,
    _find_table,
    extract_star_repositories,
    render_star_badge_files,
    render_star_badge_svg,
    update_readme_text,
)


class UpdateProfileContributionsTests(unittest.TestCase):
    def _current_pull_requests(self, readme: str) -> list[PullRequest]:
        table = _find_table(
            readme,
            ENGLISH_HEADING,
            ENGLISH_HEADER,
            ENGLISH_SEPARATOR,
        )
        pull_requests = []
        for index, url in enumerate(table.ordered_urls):
            repository, number = url.removeprefix("https://github.com/").split("/pull/")
            pull_requests.append(
                PullRequest(
                    repository=repository,
                    number=int(number),
                    title="unused for existing rows",
                    url=url,
                    merged_at=f"2026-01-{index + 1:02d}T00:00:00Z",
                )
            )
        return pull_requests

    def test_current_readme_is_idempotent(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        pull_requests = self._current_pull_requests(readme)

        self.assertEqual(update_readme_text(readme, pull_requests), readme)

    def test_current_star_badges_use_intrinsic_custom_assets(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        badge_sources = re.findall(
            r'<img src="(assets/stars/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\.svg)" '
            r'alt="[^"]+ stars">',
            readme,
        )

        self.assertGreater(len(badge_sources), 0)
        self.assertEqual(len(badge_sources), readme.count("/stargazers"))
        self.assertNotIn("img.shields.io", readme)
        for badge_source in set(badge_sources):
            badge = (ROOT / badge_source).read_text(encoding="utf-8")
            root = ElementTree.fromstring(badge)
            self.assertEqual(root.attrib["width"], str(STAR_BADGE_WIDTH))
            self.assertEqual(root.attrib["height"], str(STAR_BADGE_HEIGHT))

    def test_formats_compact_star_counts(self) -> None:
        self.assertEqual(_format_star_count(0), "0")
        self.assertEqual(_format_star_count(999), "999")
        self.assertEqual(_format_star_count(1_000), "1k")
        self.assertEqual(_format_star_count(1_500), "1.5k")
        self.assertEqual(_format_star_count(12_345), "12k")
        self.assertEqual(_format_star_count(379_000), "379k")
        self.assertEqual(_format_star_count(1_500_000), "1.5M")

    def test_renders_intrinsic_56px_star_badge(self) -> None:
        badge = render_star_badge_svg("example/project", 379_123)
        root = ElementTree.fromstring(badge)

        self.assertEqual(root.attrib["width"], str(STAR_BADGE_WIDTH))
        self.assertEqual(root.attrib["height"], str(STAR_BADGE_HEIGHT))
        self.assertEqual(root.attrib["viewBox"], "0 0 180 56")
        self.assertIn("example/project: 379,123 stars", badge)
        self.assertIn(">379k</text>", badge)

    def test_appends_new_pr_to_both_tables_and_preserves_existing_copy(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        pull_requests = self._current_pull_requests(readme)
        new_pull_request = PullRequest(
            repository="example/project",
            number=42,
            title="fix: preserve pipes | in generated table rows",
            url="https://github.com/example/project/pull/42",
            merged_at="2026-12-01T00:00:00Z",
        )

        updated = update_readme_text(readme, [*pull_requests, new_pull_request])

        original_description = (
            "Show target node name in exec-tool transparency messages so multi-agent "
            "traces stay readable when several agents share an exec channel."
        )
        self.assertIn(original_description, updated)
        self.assertEqual(updated.count(new_pull_request.url), 2)
        self.assertEqual(updated.count(r"fix: preserve pipes \| in generated table rows"), 2)
        self.assertEqual(
            update_readme_text(updated, [*pull_requests, new_pull_request]),
            updated,
        )

        english = _find_table(
            updated,
            ENGLISH_HEADING,
            ENGLISH_HEADER,
            ENGLISH_SEPARATOR,
        )
        chinese = _find_table(
            updated,
            CHINESE_HEADING,
            CHINESE_HEADER,
            CHINESE_SEPARATOR,
        )
        self.assertEqual(english.ordered_urls, chinese.ordered_urls)
        for table in (english, chinese):
            generated_row = table.rows_by_url[new_pull_request.url]
            self.assertIn('src="assets/stars/example/project.svg"', generated_row)

        repositories = extract_star_repositories(updated)
        self.assertIn(new_pull_request.repository, repositories)
        with self.assertRaisesRegex(RuntimeError, "Missing star counts"):
            render_star_badge_files(updated, {})

    def test_refuses_to_sync_when_an_existing_row_is_not_merged(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        pull_requests = self._current_pull_requests(readme)

        with self.assertRaisesRegex(RuntimeError, "not reported as merged"):
            update_readme_text(readme, pull_requests[:-1])


if __name__ == "__main__":
    unittest.main()
