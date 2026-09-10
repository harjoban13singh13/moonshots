# moonshots

A private, personal tracker. Every day, GitHub Actions snapshots which small/micro-cap
tickers are seeing unusual attention in Reddit's investing communities (via ApeWisdom's
free public API) into data/daily/. Every week, a Claude scheduled task reads the week's
snapshots, filters for real mention-volume anomalies on small/micro-cap tickers (large
caps mathematically can't 20-50x), and sends a short, clearly-speculative shortlist.

This is not investment advice and the picks are not predictions - it's a crowd-attention
anomaly detector, nothing more. Treat every weekly report as "worth a look," never as a
recommendation.

## Layout

- `scripts/ingest_daily.py` - daily pull from ApeWisdom, written to `data/daily/YYYY-MM-DD.json`
- `.github/workflows/daily-ingest.yml` - the GitHub Actions cron job that runs it
- `data/daily/` - one JSON snapshot per day
- `data/weekly/` - one report per week
- `site/` - the frontend that reads from the data (coming once there's real data to show)

## Data source

[ApeWisdom](https://apewisdom.io/api/) - free, keyless, no signup. Covers ~15 finance
subreddits including r/wallstreetbets. Returns mention counts and upvotes, not a polarity
sentiment score - the weekly synthesis step treats mention-volume spikes as the signal.

Reddit's own API was deliberately not used: as of 2026 it requires manual approval under
Reddit's Responsible Builder Policy, with personal projects the most commonly rejected
category and no published turnaround time.
