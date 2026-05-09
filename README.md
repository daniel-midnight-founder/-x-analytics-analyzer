# X Analytics Analyzer

A Claude Code skill that analyzes your X/Twitter analytics exports and generates a styled HTML report with actionable growth insights.

## What it does

- Parses your X Creator Studio CSV exports
- Categorizes posts by content type (Authority, Growth, Personality, Reply, Thread, Question)
- Analyzes hook performance and growth funnel metrics
- Generates a polished HTML report with recommendations

## Before you start

You need to export your analytics data from X first.

### Step 1 — Export Content Analytics

1. Log in to [X](https://x.com)
2. Go to **Analytics** at [x.com/i/account_analytics](https://x.com/i/account_analytics)
3. Click **Content**
4. Download the **Account content analytics** CSV

![Content Analytics Export](/images/content_analytics_download.png)

### Step 2 — Export Overview Analytics

1. In the same Analytics section, go to **Overview** tab
2. Download the **Account overview analytics** CSV

![Overview Analytics Export](/images/overview_analytics_download.png)

Save both files somewhere accessible on your computer.

## How to install — Claude Code

1. Download the `.skill` file from the [latest release](https://github.com/daniel-midnight-founder/-x-analytics-analyzer/releases/latest)
2. Unzip the file
3. Move the unzipped folder to `~/.claude/skills/` on your computer
4. The skill will appear when you type `/` in Claude Code

## How to install — Claude Desktop

1. Download the `.skill` file from the [latest release](https://github.com/daniel-midnight-founder/-x-analytics-analyzer/releases/latest)
2. In Claude Desktop, click **Customize** in the left panel
3. Click **Skills** in the left sidebar, then click the **+**
4. Select **Create Skill → Upload a skill**
5. Navigate to the downloaded `.skill` file and select it
6. The skill will be available when you type `/` in Claude Desktop

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

---

Questions or feedback? [Open an issue](https://github.com/daniel-midnight-founder/-x-analytics-analyzer/issues) or [DM me on X @MnFounder](https://x.com/MnFounder).