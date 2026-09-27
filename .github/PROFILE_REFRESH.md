# Monthly profile refresh

The `Monthly profile refresh` workflow runs at 1:17 AM on the first day of each
month in the `America/Los_Angeles` timezone. It can also be started manually
from the repository's **Actions** tab.

## What it updates

- Project and contribution Star counts are displayed as compact, plain-text
  links to each repository's Stargazers page. They inherit GitHub's normal
  table font, color, and size.
- Star counts are refreshed from GitHub during each monthly or manual run.
  Between runs, a displayed count can be up to one month behind GitHub.
- The updater searches GitHub for external pull requests authored by
  `JiataiWang` that are currently merged.
- Existing English and Chinese contribution rows are preserved byte-for-byte.
- A newly merged PR is appended to both tables with a linked Star count once
  `.github/contribution-summaries.json` contains curated English (`en`) and
  Chinese (`zh`) summaries keyed by its full PR URL. Each summary describes the
  contribution and its practical effect instead of repeating the PR title.
- PRs missing either summary are left out of both tables and reported in the
  workflow log for follow-up. Star counts continue to refresh; the updater
  never falls back to PR titles.

## Safety boundaries

- The updater only changes linked Star-count text and the two contribution
  tables below `Agent frameworks / runtime` and `Agent 框架`.
- It never edits the introduction, project descriptions, research directions,
  or existing contribution descriptions.
- It stops without writing if the English and Chinese tables differ, if the
  expected table structure changes, or if an existing row is not reported as
  merged by GitHub.
- It excludes PRs in `JiataiWang/JiataiWang`, so profile-maintenance PRs do not
  appear as open-source contributions.

## Update flow

When a displayed Star count changes or new merged PRs with bilingual summaries
are found, the workflow commits the README update directly to `main`. All
previously curated copy is left untouched. No manual review or merge is
required for these monthly updates.

To include a newly merged contribution, read the PR and add concise `en` and
`zh` summaries to `.github/contribution-summaries.json`, then run the updater
or the workflow. Edit existing contribution descriptions directly in both
README tables; changing the summary file does not overwrite existing rows.

If `main` changes after the workflow starts, Git rejects the non-fast-forward
push instead of overwriting the newer commit. The next scheduled or manual run
can then retry the update safely.

## GitHub scheduling note

GitHub may automatically disable scheduled workflows in a public repository
after 60 days without repository activity. If that happens, re-enable
`Monthly profile refresh` from the **Actions** tab and use **Run workflow** to
perform an immediate check.
