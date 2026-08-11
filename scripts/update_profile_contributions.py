#!/usr/bin/env python3
"""Append newly merged external PRs to the profile contribution tables.

Existing rows are preserved byte-for-byte so curated English and Chinese
descriptions are never rewritten by automation. New rows use the GitHub PR
title as their description; the scheduled workflow commits the update directly
to the profile repository's main branch.
"""

from __future__ import annotations

import argparse
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
STAR_BADGE_HEIGHT = 56

ENGLISH_HEADING = "##### Agent frameworks / runtime"
CHINESE_HEADING = "##### Agent 框架"
ENGLISH_HEADER = "| Project | Stars | PR | What I Did |"
ENGLISH_SEPARATOR = "|---------|:-----:|:--:|------------|"
CHINESE_HEADER = "| 项目 | Stars | PR | 修了啥 |"
CHINESE_SEPARATOR = "|------|:-----:|:--:|--------|"

PR_URL_RE = re.compile(r"https://github\.com/([^/]+/[^/]+)/pull/(\d+)")


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


def _render_star_badge(repository: str) -> str:
    repository_name = repository.split("/", 1)[-1]
    repository_url = f"https://github.com/{repository}"
    return (
        f'<a href="{repository_url}/stargazers">'
        f'<img src="https://img.shields.io/github/stars/{repository}'
        f'?style=flat&amp;label=stars" alt="{repository_name} stars" '
        f'height="{STAR_BADGE_HEIGHT}"></a>'
    )


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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readme", type=Path, default=Path("README.md"))
    parser.add_argument("--author", default=DEFAULT_AUTHOR)
    parser.add_argument("--exclude-repository", default=DEFAULT_EXCLUDED_REPOSITORY)
    parser.add_argument("--fixture", type=Path, help="Read normalized PR data from JSON instead of GitHub")
    args = parser.parse_args()

    if args.fixture:
        merged_pull_requests = _load_fixture(args.fixture)
    else:
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not token:
            parser.error("GH_TOKEN or GITHUB_TOKEN is required when --fixture is not used")
        merged_pull_requests = fetch_merged_pull_requests(
            token=token,
            author=args.author,
            excluded_repository=args.exclude_repository,
        )

    original = args.readme.read_text(encoding="utf-8")
    updated = update_readme_text(original, merged_pull_requests)
    if updated == original:
        print(f"Profile is current: {len(merged_pull_requests)} merged external PRs found.")
        return 0

    args.readme.write_text(updated, encoding="utf-8")
    added = len(set(PR_URL_RE.findall(updated)) - set(PR_URL_RE.findall(original)))
    print(f"Updated {args.readme}: appended {added} newly merged PR(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
