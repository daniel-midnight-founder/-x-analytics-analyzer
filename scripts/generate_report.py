#!/usr/bin/env python3
"""
X Analytics Report Generator
Takes a JSON file with X analytics data and outputs a styled HTML report.
"""
import json, argparse, os
from datetime import datetime

def get_perf_color(rate):
    if rate >= 8: return "#10B981"
    if rate >= 5: return "#3B82F6"
    if rate >= 3: return "#F59E0B"
    return "#EF4444"

def get_content_type_color(t):
    colors = {
        "Authority": "#3B82F6",
        "Growth": "#10B981",
        "Personality": "#8B5CF6",
        "Reply": "#06B6D4",
        "Question": "#F59E0B",
        "Thread": "#EC489E",
        "Other": "#64748B",
    }
    return colors.get(t, "#64748B")

def build_html(data):
    d = data
    handle = d.get("account_handle", "")
    date_start = d.get("date_range", {}).get("start", "")
    date_end = d.get("date_range", {}).get("end", "")
    total = d.get("total_posts", 0)
    avgs = d.get("overall_averages", {})
    imp_avg = avgs.get("impressions_per_post", 0)
    eng_avg = avgs.get("engagement_rate", 0)
    flw_avg = avgs.get("new_followers_per_post", 0)
    gf = d.get("growth_funnel", {})

    # Top posts
    def build_post_card(post):
        color = get_perf_color(post.get("engagement_rate", 0))
        ct_color = get_content_type_color(post.get("content_type", ""))
        return f'''<div class="post-card">
  <div class="post-text">{post.get("text", "")}</div>
  <div class="post-meta">
    <span class="meta-item imp">{post.get("impressions", 0):,} imp</span>
    <span class="meta-item eng" style="color:{color}">{post.get("engagement_rate", 0)}% eng</span>
    <span class="meta-item flw">{post.get("new_followers", 0)} followers</span>
  </div>
  <div class="post-tags">
    <span class="ct-tag" style="color:{ct_color};border-color:{ct_color}">{post.get("content_type", "other")}</span>
    <span class="hook-tag">{post.get("hook_type", "none")}</span>
  </div>
  <div class="post-note">{post.get("note", "")}</div>
</div>'''

    top_imp_html = "".join(build_post_card(p) for p in d.get("top_posts", {}).get("by_impressions", []))
    top_eng_html = "".join(build_post_card(p) for p in d.get("top_posts", {}).get("by_engagement", []))
    top_flw_html = "".join(build_post_card(p) for p in d.get("top_posts", {}).get("by_followers", []))

    # Content performance
    cp_html = ""
    for ct, stats in d.get("content_performance", {}).items():
        color = get_perf_color(stats.get("avg_engagement_rate", 0))
        ct_color = get_content_type_color(ct)
        cp_html += f'''<div class="cp-row">
  <span class="cp-type" style="color:{ct_color}">{ct}</span>
  <span class="cp-count">{stats.get("count", 0)} posts</span>
  <span class="cp-imp">{stats.get("avg_impressions", 0):.0f} avg imp</span>
  <span class="cp-eng" style="color:{color}">{stats.get("avg_engagement_rate", 0)}%</span>
</div>'''

    # Best days
    bd_html = ""
    for day in d.get("best_days", []):
        color = get_perf_color(day.get("avg_engagement_rate", 0))
        bd_html += f'''<div class="day-row">
  <span class="day-name">{day.get("day", "")}</span>
  <span class="day-imp">{day.get("avg_impressions", 0):.0f} avg imp</span>
  <span class="day-eng" style="color:{color}">{day.get("avg_engagement_rate", 0)}% eng</span>
</div>'''

    # Hook analysis
    ha = d.get("hook_analysis", {})
    hook_rec = ha.get("recommendation", "")
    hook_html = f'<div class="hook-rec">{hook_rec}</div>'

    # Flopped
    flopped_html = ""
    for p in d.get("flopped_posts", []):
        flopped_html += f'''<div class="flop-card">
  <div class="post-text">{p.get("text", "")}</div>
  <div class="post-meta">
    <span class="meta-item imp">{p.get("impressions", 0):,} imp</span>
    <span class="meta-item eng" style="color:#EF4444">{p.get("engagement_rate", 0)}% eng</span>
    <span class="hook-tag">{p.get("hook_type", "none")}</span>
  </div>
  <div class="flop-issue">{p.get("issue", "")}</div>
</div>'''

    # Growth funnel
    pcr = gf.get("profile_click_rate", 0)
    fcr = gf.get("follower_conversion_rate", 0)
    funnel_html = f'''<div class="funnel-grid">
  <div class="funnel-card">
    <div class="funnel-number">{pcr:.2f}%</div>
    <div class="funnel-label">Profile click rate</div>
    <div class="funnel-note">impressions that led to profile visits</div>
  </div>
  <div class="funnel-card">
    <div class="funnel-number">{fcr:.2f}%</div>
    <div class="funnel-label">Follower conversion</div>
    <div class="funnel-note">impressions that led to new follows</div>
  </div>
</div>'''

    # Recommendations
    def build_rec(item):
        return f'<div class="rec-item"><div><strong>{item.get("action","")}</strong><p>{item.get("why","")}</p><code>{item.get("data","")}</code></div></div>'

    do_more_html = "".join(build_rec(i) for i in d.get("do_more", []))
    do_less_html = "".join(build_rec(i) for i in d.get("do_less", []))
    do_diff_html = "".join(build_rec(i) for i in d.get("do_differently", []))

    today = datetime.now().strftime("%B %d, %Y")

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>X Analytics Report</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'DM Sans',sans-serif;background:#0A0A0F;color:#E2E8F0;line-height:1.7;-webkit-font-smoothing:antialiased}}
.container{{max-width:800px;margin:0 auto;padding:40px 24px 80px}}
.mono{{font-family:'Space Mono',monospace}}

.report-header{{text-align:center;padding:60px 0 40px;border-bottom:1px solid rgba(255,255,255,0.06)}}
.report-header h1{{font-size:32px;font-weight:700;letter-spacing:-0.5px;margin-bottom:8px;color:#F8FAFC}}
.report-header .handle{{font-size:20px;color:#3B82F6;margin-bottom:4px}}
.report-header .daterange{{color:#64748B;font-size:14px}}
.report-header .date{{color:#475569;font-size:12px;margin-top:12px}}

.averages-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:32px 0}}
.avg-card{{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:24px;text-align:center}}
.avg-number{{font-family:'Space Mono',monospace;font-size:36px;font-weight:700;color:#F8FAFC;line-height:1}}
.avg-label{{font-size:12px;color:#64748B;text-transform:uppercase;letter-spacing:1px;margin-top:8px}}

.section{{margin-top:48px}}
.section-label{{font-family:'Space Mono',monospace;font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#64748B;margin-bottom:8px}}
.section-title{{font-size:22px;font-weight:700;color:#F8FAFC;margin-bottom:20px}}
.section-divider{{height:1px;background:linear-gradient(90deg,rgba(255,255,255,0.08),transparent);margin-bottom:32px}}

.post-card{{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:20px;margin-bottom:12px}}
.post-text{{font-size:14px;color:#E2E8F0;margin-bottom:12px;line-height:1.6}}
.post-meta{{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:8px}}
.meta-item{{font-family:'Space Mono',monospace;font-size:13px;color:#94A3B8}}
.meta-item.imp{{color:#94A3B8}}
.meta-item.eng{{font-weight:700}}
.meta-item.flw{{color:#10B981}}
.post-tags{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}}
.ct-tag,.hook-tag{{font-family:'Space Mono',monospace;font-size:11px;padding:2px 8px;border-radius:4px;text-transform:uppercase}}
.ct-tag{{background:rgba(59,130,246,0.1)}}
.hook-tag{{background:rgba(245,158,11,0.1);color:#F59E0B}}
.post-note{{font-size:12px;color:#64748B;font-style:italic}}

.cp-row{{display:grid;grid-template-columns:120px 80px 100px 60px;gap:8px;align-items:center;padding:12px 16px;border-bottom:1px solid rgba(255,255,255,0.04);font-size:14px}}
.cp-header-row{{display:grid;grid-template-columns:120px 80px 100px 60px;gap:8px;align-items:center;padding:8px 16px;font-family:'Space Mono',monospace;font-size:11px;text-transform:uppercase;color:#64748B;border-bottom:1px solid rgba(255,255,255,0.08)}}
.cp-type{{font-weight:500;text-transform:capitalize}}
.cp-count{{color:#64748B}}
.cp-imp{{color:#94A3B8}}
.cp-eng{{font-family:'Space Mono',monospace;font-weight:700;text-align:right}}

.day-row{{display:grid;grid-template-columns:100px 1fr 80px;gap:12px;align-items:center;padding:14px 16px;background:rgba(255,255,255,0.02);border-radius:8px;margin-bottom:8px}}
.day-name{{font-weight:500;color:#CBD5E1}}
.day-imp{{color:#94A3B8}}
.day-eng{{font-family:'Space Mono',monospace;font-weight:700;text-align:right}}

.funnel-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.funnel-card{{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:24px;text-align:center}}
.funnel-number{{font-family:'Space Mono',monospace;font-size:32px;font-weight:700;color:#3B82F6;line-height:1}}
.funnel-label{{font-size:14px;font-weight:500;color:#CBD5E1;margin-top:8px}}
.funnel-note{{font-size:12px;color:#64748B;margin-top:4px}}

.hook-rec{{font-size:14px;color:#94A3B8;padding:16px 20px;background:rgba(255,255,255,0.02);border-radius:8px;line-height:1.6}}

.flop-card{{background:rgba(239,68,68,0.04);border:1px solid rgba(239,68,68,0.1);border-radius:12px;padding:20px;margin-bottom:12px}}
.flop-issue{{font-size:13px;color:#EF4444;margin-top:8px}}

.rec-item{{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:20px;margin-bottom:12px}}
.rec-item strong{{font-size:15px;color:#F8FAFC;display:block;margin-bottom:4px}}
.rec-item p{{font-size:14px;color:#94A3B8;margin-bottom:6px}}
.rec-item code{{font-family:'Space Mono',monospace;font-size:12px;color:#64748B;background:rgba(255,255,255,0.04);padding:3px 8px;border-radius:4px}}

.summary-box{{background:linear-gradient(135deg,rgba(59,130,246,0.08),rgba(139,92,246,0.06));border:1px solid rgba(59,130,246,0.15);border-radius:12px;padding:24px;font-size:16px;color:#E2E8F0;line-height:1.6;text-align:center}}

.report-footer{{text-align:center;padding:48px 0 0;margin-top:48px;border-top:1px solid rgba(255,255,255,0.06);color:#475569;font-size:12px}}
</style>
</head>
<body>
<div class="container">

<div class="report-header">
  <h1>X Analytics Report</h1>
  <div class="handle mono"><a href="https://x.com/{handle.replace('@', '')}" style="color:#3B82F6;text-decoration:none">{handle}</a></div>
  <div class="daterange">{date_start} to {date_end}</div>
  <div class="date">{today}</div>
</div>

<div class="section">
  <div class="section-label">Overview</div>
  <div class="section-title">{total} Posts Analyzed</div>
  <div class="section-divider"></div>
  <div class="averages-grid">
    <div class="avg-card">
      <div class="avg-number">{imp_avg:.0f}</div>
      <div class="avg-label">Avg Impressions</div>
    </div>
    <div class="avg-card">
      <div class="avg-number">{eng_avg:.1f}%</div>
      <div class="avg-label">Avg Engagement</div>
    </div>
    <div class="avg-card">
      <div class="avg-number">{flw_avg:.1f}</div>
      <div class="avg-label">Avg New Followers</div>
    </div>
  </div>
</div>

<div class="section">
  <div class="section-label">Growth Funnel</div>
  <div class="section-title">From Impressions to Followers</div>
  <div class="section-divider"></div>
  {funnel_html}
</div>

<div class="section">
  <div class="section-label">Top Posts</div>
  <div class="section-title">Highest Impressions</div>
  <div class="section-divider"></div>
  {top_imp_html}
</div>

<div class="section">
  <div class="section-title">Highest Engagement</div>
  <div class="section-divider"></div>
  {top_eng_html}
</div>

<div class="section">
  <div class="section-title">Most New Followers</div>
  <div class="section-divider"></div>
  {top_flw_html}
</div>

<div class="section">
  <div class="section-label">Content</div>
  <div class="section-title">Performance by Type</div>
  <div class="section-divider"></div>
  <div class="cp-header-row">
    <span>Type</span><span>Posts</span><span>Avg Imp</span><span>Eng</span>
  </div>
  {cp_html}
</div>

<div class="section">
  <div class="section-label">Timing</div>
  <div class="section-title">Best Days</div>
  <div class="section-divider"></div>
  {bd_html}
</div>

<div class="section">
  <div class="section-label">Hooks</div>
  <div class="section-title">Hook Analysis</div>
  <div class="section-divider"></div>
  {hook_html}
</div>

<div class="section">
  <div class="section-label">What Didn't Work</div>
  <div class="section-title">Flopped Posts</div>
  <div class="section-divider"></div>
  {flopped_html}
</div>

<div class="section">
  <div class="section-label">Recommendations</div>
  <div class="section-title">What to Do Next</div>
  <div class="section-divider"></div>
  {do_more_html}
  {do_less_html}
  {do_diff_html}
</div>

<div class="section">
  <div class="section-label">Summary</div>
  <div class="section-title">Bottom Line</div>
  <div class="section-divider"></div>
  <div class="summary-box">{d.get("summary", "")}</div>
</div>

<div class="report-footer">
  Built with the X Analytics Analyzer skill by <a href="https://x.com/MnFounder" style="color:#3B82F6;text-decoration:none">@MnFounder</a> &middot; {today}
</div>

</div>
</body>
</html>'''
    return html

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to JSON data file")
    parser.add_argument("--output", required=True, help="Path for output HTML file")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    html = build_html(data)

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    print(json.dumps({"status": "success", "output": args.output}))

if __name__ == "__main__":
    main()