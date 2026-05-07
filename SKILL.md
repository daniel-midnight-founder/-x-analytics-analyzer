---
name: x-analytics-analyzer
description: Use when analyzing X/Twitter analytics CSV data or wanting insights on what content performs best, what drives followers, and what to do more or less of
---

# X Analytics Analyzer

Analyzes X Creator Studio CSV exports to extract actionable growth insights. Turns raw data into specific recommendations grounded in actual post performance. The final deliverable is a **styled HTML report**.

---

## THE FLOW

**Stage 1** → Upload & Intake (understand what data was uploaded)
**Stage 2** → Data Processing (extract posts, metrics, content categories)
**Stage 3** → Analysis (top posts by impressions/engagement/followers, content type performance, timing patterns)
**Stage 4** → Recommendations (do more / do less / do differently)
**Stage 5** → Generate HTML Report

---

## STAGE 1: UPLOAD & INTAKE

Ask the user to upload their X analytics CSV from Creator Studio.

When they provide the file, open it and acknowledge what data is available:

"Got it — I can see [number] posts in this export, spanning [date range]. Let me analyze the performance data and pull out what's actually working."

Note: X Creator Studio exports typically include columns like:
- Tweet text
- Impressions
- Engagements
- Engagement rate
- New followers
- Retweets
- Replies
- Likes
- Clicks
- Date

---

## STAGE 2: DATA PROCESSING

Parse the CSV and extract:
- Total posts analyzed
- Date range of the export
- Overall averages (impressions, engagement rate, new followers per post)
- Best performing post overall
- Posts sorted by each key metric

Use the bundled `scripts/analyze_csv.py` to process the CSV, or process inline with Python.

---

## STAGE 3: ANALYSIS

Run these analyses on the data:

### Growth Funnel Analysis (from Twitter Simplified)
Map every post to the growth funnel:
- **Awareness** (getting seen) — high impressions, any engagement
- **Consideration** (getting clicks) — profile clicks from impressions
- **Conversion** (getting followers) — new followers from posts

Identify which posts drive each stage. High impressions but low profile clicks = hook problem. High clicks but no followers = profile problem.

### Content Type Performance (Twitter Simplified framework)
Categorize using Stijn's framework:
- **Authority** — shows expertise, establishes credibility and trust. Example: "The one thing most developers get wrong about API design."
- **Growth** — simple self-improvement value. Example: "Ship faster by doing less."
- **Personality** — shows authenticity, connects personally. Example: "I spent 3 hours on this tweet and it flopped."
- **Reply** — engaging with others' content (not original tweets)
- **Thread** — multi-tweet long-form content
- **Question** — asks the audience something

Calculate avg impressions and engagement rate per category.

### Top Posts by Impressions
- Sort all posts by impressions descending
- Identify the top 5
- Note: content type (Authority/Growth/Personality), topic, format, and hook used

### Top Posts by Engagement Rate
- Engagement rate = (Total engagements / Impressions) × 100
- Sort top 5 by this rate (min 5 engagements, 50 impressions for quality)
- Note: what triggered the interaction

### Top Posts by New Followers
- Sort top 5 by new followers gained
- Note: what made people follow after seeing this post

### Hook Analysis
Look at the first line of each top post. Does it:
- Spark curiosity?
- Make a claim or promise?
- Use a number or specific fact?
- Tap into an emotion (pain point or desire)?
Classify hooks as: curiosity, authority, promise, pattern interrupt, relatability, or none.

### Best Days and Times
- Group posts by day of week
- Calculate average impressions and engagement per day
- Identify top 3 performing days

### Flopped Content Analysis
- Posts with high impressions (500+) but low engagement rate (<2%)
- Posts with high impressions but low follower conversion
- Diagnose why: bad hook, wrong audience, not actionable, too dense, not relatable

---

## STAGE 4: RECOMMENDATIONS

Based on the analysis, provide:

**3 Things to Do More Of:**
- Concrete actions backed by data
- Specific to their content style
- Include the "why" — what in their data supports this
- Reference the content type that performed best

**3 Things to Stop Doing:**
- Be specific about what to cut
- Back each with data showing it didn't work

**1-2 Things to Do Differently:**
- Subtle shifts rather than wholesale changes
- Based on patterns in the data

**Hook Improvement (if hooks are weak):**
- If top posts don't have clear hooks, suggest specific hook frameworks from their best performing content
- Recommend: opening with curiosity, using numbers, making promises, or pattern interrupts

---

## STAGE 5: GENERATE THE HTML REPORT

After analysis, compile everything into JSON and use the bundled script to generate a styled HTML report.

### JSON Structure

```json
{
  "account_handle": "@username",
  "date_range": {
    "start": "YYYY-MM-DD",
    "end": "YYYY-MM-DD"
  },
  "total_posts": 150,
  "overall_averages": {
    "impressions_per_post": 2500,
    "engagement_rate": 3.2,
    "new_followers_per_post": 12
  },
  "growth_funnel": {
    "awareness_stage": {"avg_impressions": 3000, "top_posts": []},
    "consideration_stage": {"profile_click_rate": 2.1, "note": "profile clicks / impressions"},
    "conversion_stage": {"follower_conversion_rate": 0.4, "note": "new followers / impressions"}
  },
  "top_posts": {
    "by_impressions": [
      {
        "text": "Post text preview...",
        "impressions": 15000,
        "engagement_rate": 4.1,
        "new_followers": 85,
        "content_type": "Authority",
        "hook_type": "promise",
        "note": "Why it worked"
      }
    ],
    "by_engagement": [
      {
        "text": "Post text preview...",
        "impressions": 5000,
        "engagement_rate": 8.7,
        "new_followers": 42,
        "content_type": "Personality",
        "hook_type": "curiosity",
        "note": "Why it worked"
      }
    ],
    "by_followers": [
      {
        "text": "Post text preview...",
        "impressions": 12000,
        "engagement_rate": 5.2,
        "new_followers": 120,
        "content_type": "Authority",
        "hook_type": "pattern_interrupt",
        "note": "Why it worked"
      }
    ]
  },
  "content_performance": {
    "authority": {"avg_impressions": 3000, "avg_engagement_rate": 3.5, "count": 45},
    "growth": {"avg_impressions": 1800, "avg_engagement_rate": 4.2, "count": 30},
    "personality": {"avg_impressions": 1200, "avg_engagement_rate": 5.8, "count": 20},
    "reply": {"avg_impressions": 800, "avg_engagement_rate": 5.8, "count": 25},
    "thread": {"avg_impressions": 8000, "avg_engagement_rate": 4.0, "count": 5},
    "question": {"avg_impressions": 2200, "avg_engagement_rate": 6.1, "count": 20}
  },
  "best_days": [
    {"day": "Tuesday", "avg_impressions": 3200, "avg_engagement_rate": 4.1},
    {"day": "Thursday", "avg_impressions": 2900, "avg_engagement_rate": 3.8},
    {"day": "Wednesday", "avg_impressions": 2700, "avg_engagement_rate": 3.5}
  ],
  "flopped_posts": [
    {
      "text": "Post that flopped...",
      "impressions": 10000,
      "engagement_rate": 0.8,
      "hook_type": "none",
      "issue": "High impressions but very low engagement — likely a weak hook or shown to wrong audience"
    }
  ],
  "hook_analysis": {
    "strong_hooks": ["promise", "curiosity"],
    "weak_hooks": ["none", "generic statement"],
    "recommendation": "Your best performing posts open with curiosity or specific numbers. Apply the same pattern to new content."
  },
  "do_more": [
    {"action": "Post more Authority content", "why": "Authority posts averaged 3.5% engagement — your most consistent format", "data": "45 authority posts at 3.5% eng vs 3.2% overall"}
  ],
  "do_less": [
    {"action": "Reduce generic advice tweets", "why": "Posts without clear hooks averaged just 1.2% engagement", "data": "12 posts at 1.2% eng vs 3.2% overall"}
  ],
  "do_differently": [
    {"action": "Lead every post with a hook", "why": "Your top 5 posts all have strong opening lines — your flops don't", "data": "5/5 top posts have hooks vs 0/5 flopped posts"}
  ],
  "summary": "Brief 3-4 sentence summary of key findings and top recommendation"
}
```

### Generate the Report

```bash
python scripts/generate_report.py --input data.json --output /path/to/x-analytics-report.html
```

Save the HTML file and provide a link.

After generating the report, give a brief verbal summary in chat (3-4 sentences max) with the overall score and link to the full report.

---

## ANALYSIS RULES

- Every insight must be backed by actual numbers from the CSV
- Quote real post text when describing what worked
- Be specific about which content types performed and why
- If something flopped, say so directly — don't soften it
- Focus on actionable recommendations, not generic advice
- When analyzing hooks: look at the FIRST LINE of each post, not the full text

## STYLE RULES

- Talk like a smart friend who knows X analytics, not a corporate social media consultant
- Use specific numbers everywhere
- The report should feel like it was made by someone who actually uses X
- Keep insights tight — if a post didn't work, say why in one sentence
- Write like a human, not a robot — short sentences, no corporate tone
- Never use dashes in the middle of sentences
