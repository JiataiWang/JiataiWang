# Monthly profile refresh

The `Monthly profile refresh` workflow runs at 1:17 AM on the first day of each
month in the `America/Los_Angeles` timezone. It can also be started manually
from the repository's **Actions** tab.

## What it updates

- Project and contribution star badges already read live data from Shields.io,
  so no scheduled rewrite is needed for star counts.
- The updater searches GitHub for external pull requests authored by
  `JiataiWang` that are currently merged.
- Existing English and Chinese contribution rows are preserved byte-for-byte.
- A newly merged PR is appended to both tables with a live star badge and the
  PR title as its initial description.

## Safety boundaries

- The updater only touches the two contribution tables below
  `Agent frameworks / runtime` and `Agent 框架`.
- It never edits the introduction, project tables, research directions, or
  existing contribution descriptions.
- It stops without writing if the English and Chinese tables differ, if the
  expected table structure changes, or if an existing row is not reported as
  merged by GitHub.
- It excludes PRs in `JiataiWang/JiataiWang`, so profile-maintenance PRs do not
  appear as open-source contributions.

## Review flow

When new merged PRs are found, the workflow opens a **draft pull request**. The
new English and Chinese descriptions initially use the PR title. Review and
polish those new descriptions before merging; all previously curated copy is
left untouched.

If an earlier monthly refresh PR is still open, the next run fails with a link
to that PR instead of creating a duplicate.

## GitHub scheduling note

GitHub may automatically disable scheduled workflows in a public repository
after 60 days without repository activity. If that happens, re-enable
`Monthly profile refresh` from the **Actions** tab and use **Run workflow** to
perform an immediate check.
