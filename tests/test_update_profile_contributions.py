from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from update_profile_contributions import (  # noqa: E402
    CHINESE_HEADING,
    CHINESE_TABLE_MARKER,
    ENGLISH_HEADING,
    ENGLISH_TABLE_MARKER,
    PullRequest,
    _find_table,
    _format_star_count,
    extract_star_repositories,
    update_readme_text,
    update_star_count_links,
)


class UpdateProfileContributionsTests(unittest.TestCase):
    def _current_pull_requests(self, readme: str) -> list[PullRequest]:
        table = _find_table(
            readme,
            ENGLISH_HEADING,
            ENGLISH_TABLE_MARKER,
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

    def test_current_star_counts_are_star_prefixed_plain_links(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        star_links = re.findall(
            r'<a href="https://github\.com/'
            r'([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/stargazers">([^<]+)</a>',
            readme,
        )

        self.assertGreater(len(star_links), 0)
        self.assertEqual(len(star_links), readme.count("/stargazers"))
        self.assertTrue(
            all(
                re.fullmatch(r"★ \d+(?:\.\d+)?[kMB]?", count)
                for _, count in star_links
            )
        )
        self.assertNotIn("<img", readme)
        self.assertNotIn("assets/stars", readme)
        self.assertNotIn('<th width="', readme)
        self.assertNotIn('<td width="', readme)
        self.assertEqual(readme.count('<th align="center">Stars</th>'), 4)

        star_cells = re.findall(
            r'<td align="center"><a href="https://github\.com/'
            r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/stargazers">[^<]+</a></td>',
            readme,
        )
        self.assertEqual(len(star_cells), len(star_links))

    def test_formats_compact_star_counts(self) -> None:
        self.assertEqual(_format_star_count(0), "0")
        self.assertEqual(_format_star_count(999), "999")
        self.assertEqual(_format_star_count(1_000), "1k")
        self.assertEqual(_format_star_count(1_500), "1.5k")
        self.assertEqual(_format_star_count(12_345), "12k")
        self.assertEqual(_format_star_count(379_000), "379k")
        self.assertEqual(_format_star_count(1_500_000), "1.5M")

    def test_updates_all_linked_star_counts(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        repositories = extract_star_repositories(readme)
        star_counts = {
            repository: 379_123 + index
            for index, repository in enumerate(repositories)
        }

        updated = update_star_count_links(readme, star_counts)

        for repository, star_count in star_counts.items():
            expected = (
                f'<a href="https://github.com/{repository}/stargazers">'
                f"★ {_format_star_count(star_count)}</a>"
            )
            self.assertIn(expected, updated)
        self.assertEqual(update_star_count_links(updated, star_counts), updated)

        with self.assertRaisesRegex(RuntimeError, "Missing star counts"):
            update_star_count_links(readme, {})

    def test_appends_new_pr_to_both_tables_and_preserves_existing_copy(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        pull_requests = self._current_pull_requests(readme)
        new_pull_request = PullRequest(
            repository="example/project",
            number=42,
            title="fix: preserve pipes | and <tags> in generated table rows",
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
        self.assertEqual(
            updated.count("fix: preserve pipes | and &lt;tags&gt; in generated table rows"),
            2,
        )
        self.assertEqual(
            update_readme_text(updated, [*pull_requests, new_pull_request]),
            updated,
        )

        english = _find_table(
            updated,
            ENGLISH_HEADING,
            ENGLISH_TABLE_MARKER,
        )
        chinese = _find_table(
            updated,
            CHINESE_HEADING,
            CHINESE_TABLE_MARKER,
        )
        self.assertEqual(english.ordered_urls, chinese.ordered_urls)
        for table in (english, chinese):
            generated_row = table.rows_by_url[new_pull_request.url]
            self.assertIn(
                'href="https://github.com/example/project/stargazers">★ 0</a>',
                generated_row,
            )
            self.assertNotIn("<img", generated_row)

        repositories = extract_star_repositories(updated)
        self.assertIn(new_pull_request.repository, repositories)
        star_counts = {repository: 42 for repository in repositories}
        refreshed = update_star_count_links(updated, star_counts)
        self.assertEqual(
            refreshed.count(
                '<a href="https://github.com/example/project/stargazers">★ 42</a>'
            ),
            2,
        )

    def test_refuses_to_sync_when_an_existing_row_is_not_merged(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        pull_requests = self._current_pull_requests(readme)

        with self.assertRaisesRegex(RuntimeError, "not reported as merged"):
            update_readme_text(readme, pull_requests[:-1])

    def test_refuses_an_unmarked_contribution_table(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        malformed = readme.replace(ENGLISH_TABLE_MARKER, "", 1)

        with self.assertRaisesRegex(RuntimeError, "Missing contribution table marker"):
            _find_table(malformed, ENGLISH_HEADING, ENGLISH_TABLE_MARKER)


if __name__ == "__main__":
    unittest.main()
