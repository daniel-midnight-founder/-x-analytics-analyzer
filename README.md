# X Analytics Analyzer

A Claude Code skill that analyzes your X/Twitter analytics exports and generates a styled HTML report with actionable growth insights.

## What it does

- Parses your X Creator Studio CSV exports
- Categorizes posts by content type (Authority, Growth, Personality, Reply, Thread, Question)
- Analyzes hook performance and growth funnel metrics
- Generates a polished HTML report with recommendations

## Before you start

You need to export your analytics data from X Creator Studio first.

### Step 1 — Export Content Analytics

1. Log in to [X Creator Studio](https://studio.x.com)
2. Go to **Analytics** → **Content**
3. Click **Export data** (top right)
4. Download the **Account content analytics** CSV

![Content Analytics Export](/images/content_analytics_download.png)

### Step 2 — Export Overview Analytics

1. In the same Analytics section, go to **Posts** or the Overview tab
2. Click **Export data** again
3. Download the **Account overview analytics** CSV

![Overview Analytics Export](/images/overview_analytics_download.png)

Save both files somewhere accessible on your computer.

## How to install

1. Download the `.skill` file from the [latest release](https://github.com/daniel-midnight-founder/-x-analytics-analyzer/releases/latest)
2. In Claude Code, go to **Settings** → **Skills**
3. Click **Install skill** and select the downloaded `.skill` file

## How to use

Once installed, just run the skill and point it to your CSV files:

```
/x-analytics-analyzer /path/to/account_content_analytics.csv /path/to/account_overview_analytics.csv
```

The report will be generated and saved to your desktop.

## What the report shows

- **Overall averages** — impressions, engagement rate, new followers per post
- **Growth funnel** — profile click rate and follower conversion
- **Top posts** — by impressions, engagement, and new followers
- **Content performance** — breakdown by type
- **Best days** — which days your content performs best
- **Hook analysis** — which opening patterns drive engagement
- **Flopped posts** — high reach but low engagement
- **Recommendations** — do more / do less / do differently

## Built with

The [Twitter Simplified](https://twittersimplified.com) framework by Stijn Noorman. The analysis, content categorization, and recommendations are grounded in his growth system.

---

Questions or feedback? Open an issue on GitHub.
