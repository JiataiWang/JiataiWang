#!/usr/bin/env python3
"""Refresh merged external PRs and custom Star badges in the profile.

Existing rows are preserved byte-for-byte so curated English and Chinese
descriptions are never rewritten by automation. New rows use the GitHub PR
title as their description. Each referenced repository's current star count is
rendered into an intrinsic 56px SVG; the scheduled workflow commits verified
updates directly to the profile repository's main branch.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


GITHUB_API = "https://api.github.com"
API_VERSION = "2022-11-28"
DEFAULT_AUTHOR = "JiataiWang"
DEFAULT_EXCLUDED_REPOSITORY = "JiataiWang/JiataiWang"
STAR_BADGE_DIRECTORY = Path("assets/stars")
STAR_BADGE_HEIGHT = 56
STAR_BADGE_WIDTH = 180
STAR_BADGE_LABEL_WIDTH = 104

ENGLISH_HEADING = "##### Agent frameworks / runtime"
CHINESE_HEADING = "##### Agent 框架"
ENGLISH_HEADER = "| Project | Stars | PR | What I Did |"
ENGLISH_SEPARATOR = "|---------|:-----:|:--:|------------|"
CHINESE_HEADER = "| 项目 | Stars | PR | 修了啥 |"
CHINESE_SEPARATOR = "|------|:-----:|:--:|--------|"

PR_URL_RE = re.compile(r"https://github\.com/([^/]+/[^/]+)/pull/(\d+)")
STARGAZERS_URL_RE = re.compile(
    r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/stargazers"
)
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


@dataclass(frozen=True)
class PullRequest:
    repository: str
    number: int
    title: str
    url: str
    merged_at: str = ""


@dataclass(frozen=True)
class ContributionTable:
    start: int
    end: int
    header: str
    separator: str
    rows_by_url: dict[str, str]
    ordered_urls: tuple[str, ...]


def _request_json(url: str, token: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "JiataiWang-profile-refresh",
            "X-GitHub-Api-Version": API_VERSION,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API request failed ({error.code}): {detail}") from error


def fetch_merged_pull_requests(
    token: str,
    author: str = DEFAULT_AUTHOR,
    excluded_repository: str = DEFAULT_EXCLUDED_REPOSITORY,
) -> list[PullRequest]:
    query = f"is:pr author:{author} is:merged -repo:{excluded_repository}"
    pull_requests: dict[str, PullRequest] = {}

    for page in range(1, 11):
        params = urllib.parse.urlencode(
            {
                "q": query,
                "sort": "created",
                "order": "asc",
                "per_page": 100,
                "page": page,
            }
        )
        payload = _request_json(f"{GITHUB_API}/search/issues?{params}", token)
        items = payload.get("items", [])

        if page == 1 and payload.get("total_count", 0) > 1000:
            raise RuntimeError("GitHub search returned more than 1,000 merged PRs; refusing a partial sync")

        for item in items:
            pull_request_data = item.get("pull_request") or {}
            if not pull_request_data.get("merged_at"):
                continue

            repository_url = item.get("repository_url", "")
            repository_prefix = f"{GITHUB_API}/repos/"
            if not repository_url.startswith(repository_prefix):
                raise RuntimeError(f"Unexpected repository URL: {repository_url}")

            repository = repository_url.removeprefix(repository_prefix)
            if repository.casefold() == excluded_repository.casefold():
                continue

            pull_request = PullRequest(
                repository=repository,
                number=int(item["number"]),
                title=str(item["title"]).strip(),
                url=str(item["html_url"]),
                merged_at=str(pull_request_data["merged_at"]),
            )
            pull_requests[pull_request.url] = pull_request

        if len(items) < 100:
            break
    else:
        raise RuntimeError("GitHub search pagination reached its safety limit")

    return sorted(
        pull_requests.values(),
        key=lambda pull_request: (
            pull_request.merged_at,
            pull_request.repository.casefold(),
            pull_request.number,
        ),
    )


def _validate_repository(repository: str) -> None:
    if not REPOSITORY_RE.fullmatch(repository):
        raise RuntimeError(f"Invalid GitHub repository name: {repository}")
    owner, name = repository.split("/", 1)
    if owner in {".", ".."} or name in {".", ".."}:
        raise RuntimeError(f"Invalid GitHub repository name: {repository}")


def fetch_star_counts(token: str, repositories: list[str]) -> dict[str, int]:
    star_counts: dict[str, int] = {}
    for repository in repositories:
        _validate_repository(repository)
        encoded_repository = urllib.parse.quote(repository, safe="/")
        payload = _request_json(f"{GITHUB_API}/repos/{encoded_repository}", token)

        full_name = str(payload.get("full_name", ""))
        if full_name.casefold() != repository.casefold():
            raise RuntimeError(
                f"GitHub returned repository {full_name!r} while refreshing {repository!r}"
            )

        star_count = payload.get("stargazers_count")
        if isinstance(star_count, bool) or not isinstance(star_count, int) or star_count < 0:
            raise RuntimeError(f"Invalid star count for {repository}: {star_count!r}")
        star_counts[repository] = star_count

    return star_counts


def _find_table(
    readme: str,
    heading: str,
    header: str,
    separator: str,
) -> ContributionTable:
    heading_index = readme.find(heading)
    if heading_index < 0:
        raise RuntimeError(f"Missing README heading: {heading}")

    table_start = readme.find(header, heading_index + len(heading))
    if table_start < 0:
        raise RuntimeError(f"Missing contribution table header after: {heading}")

    table_end = readme.find("\n\n", table_start)
    if table_end < 0:
        table_end = len(readme)

    lines = readme[table_start:table_end].splitlines()
    if len(lines) < 2 or lines[0] != header or lines[1] != separator:
        raise RuntimeError(f"Unexpected contribution table structure after: {heading}")

    rows_by_url: dict[str, str] = {}
    ordered_urls: list[str] = []
    for row in lines[2:]:
        matches = PR_URL_RE.findall(row)
        if len(matches) != 1:
            raise RuntimeError(f"Expected exactly one PR link in contribution row: {row}")
        repository, number = matches[0]
        url = f"https://github.com/{repository}/pull/{number}"
        if url in rows_by_url:
            raise RuntimeError(f"Duplicate PR row: {url}")
        rows_by_url[url] = row
        ordered_urls.append(url)

    return ContributionTable(
        start=table_start,
        end=table_end,
        header=header,
        separator=separator,
        rows_by_url=rows_by_url,
        ordered_urls=tuple(ordered_urls),
    )


def _escape_table_cell(value: str) -> str:
    return " ".join(value.split()).replace("|", r"\|")


def _star_badge_asset_path(
    repository: str,
    badge_directory: Path = STAR_BADGE_DIRECTORY,
) -> Path:
    _validate_repository(repository)
    owner, name = repository.split("/", 1)
    return badge_directory / owner / f"{name}.svg"


def _render_star_badge(repository: str) -> str:
    _validate_repository(repository)
    repository_name = repository.split("/", 1)[-1]
    repository_url = f"https://github.com/{repository}"
    badge_source = _star_badge_asset_path(repository).as_posix()
    return (
        f'<a href="{repository_url}/stargazers">'
        f'<img src="{badge_source}" width="{STAR_BADGE_WIDTH}" '
        f'height="{STAR_BADGE_HEIGHT}" alt="{repository_name} stars"></a>'
    )


def extract_star_repositories(readme: str) -> list[str]:
    repositories = set(STARGAZERS_URL_RE.findall(readme))
    for repository in repositories:
        _validate_repository(repository)
    return sorted(repositories, key=str.casefold)


def _format_star_count(star_count: int) -> str:
    if isinstance(star_count, bool) or not isinstance(star_count, int) or star_count < 0:
        raise ValueError(f"Invalid star count: {star_count!r}")
    if star_count < 1_000:
        return str(star_count)

    for divisor, suffix in ((1_000_000_000, "B"), (1_000_000, "M"), (1_000, "k")):
        if star_count >= divisor:
            value = star_count / divisor
            precision = 1 if value < 10 and not value.is_integer() else 0
            return f"{value:.{precision}f}{suffix}"

    raise AssertionError("Unreachable star-count formatting branch")


def render_star_badge_svg(repository: str, star_count: int) -> str:
    _validate_repository(repository)
    compact_count = _format_star_count(star_count)
    title = html.escape(f"{repository}: {star_count:,} stars")
    aria_label = html.escape(f"{repository}: {star_count:,} stars", quote=True)
    message_width = STAR_BADGE_WIDTH - STAR_BADGE_LABEL_WIDTH
    label_center = STAR_BADGE_LABEL_WIDTH / 2
    message_center = STAR_BADGE_LABEL_WIDTH + message_width / 2

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{STAR_BADGE_WIDTH}" height="{STAR_BADGE_HEIGHT}" viewBox="0 0 {STAR_BADGE_WIDTH} {STAR_BADGE_HEIGHT}" role="img" aria-label="{aria_label}">
  <title>{title}</title>
  <defs>
    <clipPath id="badge-clip">
      <rect width="{STAR_BADGE_WIDTH}" height="{STAR_BADGE_HEIGHT}" rx="8"/>
    </clipPath>
  </defs>
  <g clip-path="url(#badge-clip)">
    <rect width="{STAR_BADGE_LABEL_WIDTH}" height="{STAR_BADGE_HEIGHT}" fill="#555"/>
    <rect x="{STAR_BADGE_LABEL_WIDTH}" width="{message_width}" height="{STAR_BADGE_HEIGHT}" fill="#0969da"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision">
    <text x="{label_center:g}" y="36" font-size="22">stars</text>
    <text x="{message_center:g}" y="36" font-size="23" font-weight="700">{compact_count}</text>
  </g>
</svg>
"""


def render_star_badge_files(
    readme: str,
    star_counts: dict[str, int],
    badge_directory: Path = STAR_BADGE_DIRECTORY,
) -> dict[Path, str]:
    repositories = extract_star_repositories(readme)
    missing_repositories = set(repositories) - set(star_counts)
    if missing_repositories:
        missing = ", ".join(sorted(missing_repositories, key=str.casefold))
        raise RuntimeError(f"Missing star counts for README repositories: {missing}")

    return {
        _star_badge_asset_path(repository, badge_directory): render_star_badge_svg(
            repository,
            star_counts[repository],
        )
        for repository in repositories
    }


def _render_new_row(pull_request: PullRequest, language: str) -> str:
    repository = pull_request.repository
    repository_url = f"https://github.com/{repository}"
    stars = _render_star_badge(repository)
    description = _escape_table_cell(pull_request.title)

    if language == "en":
        return (
            f"| [{repository}]({repository_url}) | {stars} | "
            f"[#{pull_request.number}]({pull_request.url}) | {description} |"
        )
    if language == "zh":
        return (
            f"| [{repository}]({repository_url}) | {stars} | "
            f"[#{pull_request.number}]({pull_request.url}) | {description} |"
        )
    raise ValueError(f"Unsupported language: {language}")


def _replace_table(readme: str, table: ContributionTable, rows: list[str]) -> str:
    replacement = "\n".join([table.header, table.separator, *rows])
    return f"{readme[:table.start]}{replacement}{readme[table.end:]}"


def update_readme_text(readme: str, merged_pull_requests: list[PullRequest]) -> str:
    english = _find_table(
        readme,
        ENGLISH_HEADING,
        ENGLISH_HEADER,
        ENGLISH_SEPARATOR,
    )
    chinese = _find_table(
        readme,
        CHINESE_HEADING,
        CHINESE_HEADER,
        CHINESE_SEPARATOR,
    )

    if english.ordered_urls != chinese.ordered_urls:
        raise RuntimeError("English and Chinese contribution tables are out of sync")

    merged_by_url = {pull_request.url: pull_request for pull_request in merged_pull_requests}
    missing_from_github = set(english.ordered_urls) - set(merged_by_url)
    if missing_from_github:
        missing = ", ".join(sorted(missing_from_github))
        raise RuntimeError(f"Existing README rows are not reported as merged by GitHub: {missing}")

    new_pull_requests = [
        pull_request
        for pull_request in merged_pull_requests
        if pull_request.url not in english.rows_by_url
    ]
    if not new_pull_requests:
        return readme

    english_rows = [english.rows_by_url[url] for url in english.ordered_urls]
    english_rows.extend(_render_new_row(pull_request, "en") for pull_request in new_pull_requests)
    updated = _replace_table(readme, english, english_rows)

    chinese = _find_table(
        updated,
        CHINESE_HEADING,
        CHINESE_HEADER,
        CHINESE_SEPARATOR,
    )
    chinese_rows = [chinese.rows_by_url[url] for url in chinese.ordered_urls]
    chinese_rows.extend(_render_new_row(pull_request, "zh") for pull_request in new_pull_requests)
    updated = _replace_table(updated, chinese, chinese_rows)

    updated_english = _find_table(
        updated,
        ENGLISH_HEADING,
        ENGLISH_HEADER,
        ENGLISH_SEPARATOR,
    )
    updated_chinese = _find_table(
        updated,
        CHINESE_HEADING,
        CHINESE_HEADER,
        CHINESE_SEPARATOR,
    )
    if updated_english.ordered_urls != updated_chinese.ordered_urls:
        raise RuntimeError("Generated English and Chinese contribution tables differ")

    return updated


def _load_fixture(path: Path) -> list[PullRequest]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [PullRequest(**item) for item in data]


def _load_star_fixture(path: Path) -> dict[str, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError("Star fixture must be a JSON object mapping repositories to counts")

    star_counts: dict[str, int] = {}
    for repository, star_count in data.items():
        _validate_repository(repository)
        if isinstance(star_count, bool) or not isinstance(star_count, int) or star_count < 0:
            raise RuntimeError(f"Invalid fixture star count for {repository}: {star_count!r}")
        star_counts[repository] = star_count
    return star_counts


def _write_text_if_changed(path: Path, content: str) -> bool:
    try:
        original = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        original = None
    if original == content:
        return False

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readme", type=Path, default=Path("README.md"))
    parser.add_argument("--author", default=DEFAULT_AUTHOR)
    parser.add_argument("--exclude-repository", default=DEFAULT_EXCLUDED_REPOSITORY)
    parser.add_argument("--fixture", type=Path, help="Read normalized PR data from JSON instead of GitHub")
    parser.add_argument(
        "--star-fixture",
        type=Path,
        help="Read repository-to-star-count data from JSON instead of GitHub",
    )
    args = parser.parse_args()

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if (not args.fixture or not args.star_fixture) and not token:
        parser.error(
            "GH_TOKEN or GITHUB_TOKEN is required unless both PR and star fixtures are used"
        )

    if args.fixture:
        merged_pull_requests = _load_fixture(args.fixture)
    else:
        merged_pull_requests = fetch_merged_pull_requests(
            token=str(token),
            author=args.author,
            excluded_repository=args.exclude_repository,
        )

    original = args.readme.read_text(encoding="utf-8")
    updated = update_readme_text(original, merged_pull_requests)

    repositories = extract_star_repositories(updated)
    if args.star_fixture:
        star_counts = _load_star_fixture(args.star_fixture)
    else:
        star_counts = fetch_star_counts(str(token), repositories)
    badge_files = render_star_badge_files(updated, star_counts)

    readme_changed = _write_text_if_changed(args.readme, updated)
    changed_badges = sum(
        _write_text_if_changed(path, content) for path, content in badge_files.items()
    )
    added = len(set(PR_URL_RE.findall(updated)) - set(PR_URL_RE.findall(original)))
    if not readme_changed and not changed_badges:
        print(
            f"Profile is current: {len(merged_pull_requests)} merged external PRs and "
            f"{len(badge_files)} star badges checked."
        )
        return 0

    print(
        f"Updated profile: appended {added} newly merged PR(s) and refreshed "
        f"{changed_badges} star badge(s)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
