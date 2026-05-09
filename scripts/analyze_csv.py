#!/usr/bin/env python3
"""
X Analytics CSV Analyzer
Parses X Creator Studio CSV exports and outputs JSON for the HTML report generator.
"""
import csv
import json
import sys
import re
from collections import defaultdict
from datetime import datetime

def hook_type(text):
    """Classify the hook type based on the first line of the post.

    For replies, we look at the content AFTER the @mention.
    The @username is not the hook — your words after it are.
    """
    first_line = text.strip().split('\n')[0][:200]
    is_reply = text.strip().startswith('@')

    if is_reply:
        stripped = text.strip()
        at_pos = stripped.find('@')
        if at_pos >= 0:
            rest = stripped[at_pos:]
            space_pos = rest.find(' ')
            if space_pos > 0:
                first_line = rest[space_pos+1:].strip()[:200]
            else:
                first_line = rest[1:].strip()[:200]
        if not first_line:
            return 'none'
    else:
        first_line = first_line[:200]

    first_lower = first_line.lower()

    if any(word in first_lower for word in ['everyone thinks', 'you probably', 'stop doing', 'most people', 'nobody tells', 'here is the thing']):
        return 'pattern_interrupt'
    if any(word in first_lower for word in ['how to', 'the way to', 'the secret', 'this is how', "here's how", 'the reason', 'the problem']):
        return 'promise'
    if any(word in first_lower for word in ['why ', 'what if', 'imagine ', 'have you ever', 'did you know', "the question isn't", "it's not about"]):
        return 'curiosity'
    if re.match(r'^\d+', first_line.strip()) or re.match(r'^\d+x', first_line.strip()):
        return 'number'
    if any(word in first_lower for word in ['the truth about', 'my experience', 'after 1000+', 'lessons from', 'what nobody']):
        return 'authority'
    if any(word in first_lower for word in ['i tried', 'i spent', 'i realized', 'my biggest', "i've been", 'i quit']):
        return 'relatability'
    if len(first_line.strip()) < 10:
        return 'none'
    return 'none'

def categorize(text):
    """Categorize content into types based on structure and keywords."""
    text_lower = text.lower()
    lines = text.strip().split('\n')

    if text.strip().startswith('@'):
        return 'Reply'
    if len(lines) > 3 or (len(text) > 280 and '\n' in text):
        return 'Thread'
    if '?' in text and any(word in text_lower for word in ['you', 'what', 'how', 'when', 'where', 'why', 'should']):
        return 'Question'
    if any(word in text_lower for word in ["here's what", 'the truth is', "most people don't", 'the key insight', 'lesson:', 'mistake:', 'what i learned', 'my experience']):
        return 'Authority'
    if any(word in text_lower for word in ['ship faster', 'do less', 'focus on', 'start with', 'the best way', 'stop ', 'tip:', 'rule:', 'hack:']) and len(text) < 280:
        return 'Growth'
    if any(word in text_lower for word in ['i tried', 'i spent', 'i realized', 'i quit', 'i built', 'i launched', 'my biggest', 'story:', 'behind the scenes', 'honestly', "i've been"]):
        return 'Personality'
    return 'Other'

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_csv.py <csv_file> [output_json]")
        sys.exit(1)

    csv_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    posts = []
    with open(csv_path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                impressions = int(row.get('Impressions', 0) or 0)
                engagements = int(row.get('Engagements', 0) or 0)
                new_followers = int(row.get('New follows', 0) or 0)
                profile_visits = int(row.get('Profile visits', 0) or 0)
                eng_rate = (engagements / impressions * 100) if impressions > 0 else 0

                date_str = row.get('Date', '')
                try:
                    date_obj = datetime.strptime(date_str, '%a, %b %d, %Y')
                    day_of_week = date_obj.strftime('%A')
                except:
                    day_of_week = 'Unknown'

                post_text = row.get('Post text', '')
                content_type = categorize(post_text)
                hook = hook_type(post_text)

                posts.append({
                    'text': post_text,
                    'date': date_str,
                    'date_obj': date_obj,
                    'day_of_week': day_of_week,
                    'impressions': impressions,
                    'engagements': engagements,
                    'eng_rate': eng_rate,
                    'new_followers': new_followers,
                    'profile_visits': profile_visits,
                    'content_type': content_type,
                    'hook_type': hook,
                })
            except Exception as e:
                pass

    if not posts:
        print("No posts parsed")
        return

    # Overall stats
    total_impressions = sum(p['impressions'] for p in posts)
    total_engagements = sum(p['engagements'] for p in posts)
    total_new_followers = sum(p['new_followers'] for p in posts)
    total_profile_visits = sum(p['profile_visits'] for p in posts)
    avg_impressions = total_impressions / len(posts) if posts else 0
    avg_eng_rate = (total_engagements / total_impressions * 100) if total_impressions > 0 else 0
    avg_new_followers = total_new_followers / len(posts) if posts else 0
    profile_click_rate = (total_profile_visits / total_impressions * 100) if total_impressions > 0 else 0
    follower_conversion = (total_new_followers / total_impressions * 100) if total_impressions > 0 else 0

    dates = [p['date_obj'] for p in posts if p.get('date_obj')]
    date_range = (min(dates), max(dates)) if dates else (None, None)

    reply_count = sum(1 for p in posts if p['content_type'] == 'Reply')
    follower_count = sum(1 for p in posts if p['new_followers'] > 0)

    # Top posts
    by_impressions = [p for p in sorted(posts, key=lambda x: x['impressions'], reverse=True) if p['impressions'] >= 100][:5]
    by_eng_rate = [p for p in sorted(posts, key=lambda x: x['eng_rate'], reverse=True) if p['engagements'] >= 5 and p['impressions'] >= 50][:5]
    by_followers = [p for p in sorted(posts, key=lambda x: x['new_followers'], reverse=True) if p['new_followers'] > 0][:5]

    # Content type performance
    type_stats = defaultdict(lambda: {'impressions': [], 'eng_rates': [], 'count': 0})
    for p in posts:
        ct = p['content_type']
        type_stats[ct]['impressions'].append(p['impressions'])
        type_stats[ct]['eng_rates'].append(p['eng_rate'])
        type_stats[ct]['count'] += 1

    content_performance = {}
    for ct, stats in type_stats.items():
        avg_imp = sum(stats['impressions']) / len(stats['impressions']) if stats['impressions'] else 0
        avg_eng = sum(stats['eng_rates']) / len(stats['eng_rates']) if stats['eng_rates'] else 0
        content_performance[ct.lower()] = {
            'avg_impressions': round(avg_imp, 0),
            'avg_engagement_rate': round(avg_eng, 2),
            'count': stats['count']
        }

    # Best days
    day_stats = defaultdict(lambda: {'impressions': [], 'eng_rates': [], 'count': 0})
    for p in posts:
        day = p['day_of_week']
        day_stats[day]['impressions'].append(p['impressions'])
        day_stats[day]['eng_rates'].append(p['eng_rate'])
        day_stats[day]['count'] += 1

    best_days = []
    for day, stats in day_stats.items():
        avg_imp = sum(stats['impressions']) / len(stats['impressions'])
        avg_eng = sum(stats['eng_rates']) / len(stats['eng_rates'])
        best_days.append({'day': day, 'avg_impressions': round(avg_imp, 0), 'avg_engagement_rate': round(avg_eng, 2)})

    best_days.sort(key=lambda x: x['avg_impressions'], reverse=True)

    # Hook analysis — only for non-reply posts (where hooks are actually measurable)
    original_posts = [p for p in posts if p['content_type'] != 'Reply']
    reply_posts = [p for p in posts if p['content_type'] == 'Reply']

    hook_counts = defaultdict(lambda: {'count': 0, 'avg_eng': []})
    for p in original_posts:
        ht = p['hook_type']
        hook_counts[ht]['count'] += 1
        hook_counts[ht]['avg_eng'].append(p['eng_rate'])

    hook_performance = {}
    for ht, stats in hook_counts.items():
        avg_eng = sum(stats['avg_eng']) / len(stats['avg_eng']) if stats['avg_eng'] else 0
        hook_performance[ht] = {'count': stats['count'], 'avg_engagement': round(avg_eng, 2)}

    # Only call something a "strong hook" if it has real sample size
    strong_hooks = [ht for ht, stats in hook_performance.items() if stats['avg_engagement'] > avg_eng_rate and stats['count'] >= 3]
    weak_hooks = [ht for ht, stats in hook_performance.items() if stats['avg_engagement'] < avg_eng_rate * 0.7 and stats['count'] >= 3]

    # Build dynamic hook recommendation from actual data
    hook_rec_parts = []
    if original_posts:
        total_original = len(original_posts)
        reply_pct = len(reply_posts) / len(posts) * 100
        hook_rec_parts.append(f"You posted {total_original} original posts and {len(reply_posts)} replies ({reply_pct:.0f}% replies).")

    if strong_hooks:
        hook_rec_parts.append(f"Your strongest hooks on original posts: {', '.join(strong_hooks)}.")
    if weak_hooks:
        hook_rec_parts.append(f"Your weakest hooks: {', '.join(weak_hooks)} — consider dropping these patterns.")
    if not strong_hooks and not weak_hooks and hook_performance:
        hook_rec_parts.append(f"Your original posts used these hooks: {', '.join(hook_performance.keys())}.")

    if reply_posts and len(reply_posts) / len(posts) > 0.7:
        hook_rec_parts.append("Your reply strategy is correct for your follower stage. Below 3K followers, commenting drives most growth.")

    hook_recommendation = ' '.join(hook_rec_parts) if hook_rec_parts else "No strong hook pattern detected yet."

    # Flopped posts
    flopped = [p for p in posts if p['impressions'] >= 500 and p['eng_rate'] < 2]
    flopped = sorted(flopped, key=lambda x: x['impressions'], reverse=True)[:5]

    # Recommendations
    do_more = []
    do_less = []
    do_differently = []

    # Content type recommendation
    type_avg_eng = {}
    for ct, stats in type_stats.items():
        avg_eng = sum(stats['eng_rates']) / len(stats['eng_rates']) if stats['eng_rates'] else 0
        type_avg_eng[ct] = (avg_eng, stats['count'])

    if type_avg_eng:
        best_types = sorted(type_avg_eng.items(), key=lambda x: x[1][0], reverse=True)
        if best_types and best_types[0][1][1] >= 5:
            top_type, (top_eng, top_count) = best_types[0]
            do_more.append({
                'action': f'Post more {top_type} content',
                'why': f'{top_type} posts averaged {top_eng:.1f}% engagement rate',
                'data': f"{top_count} {top_type} posts at {top_eng:.1f}% avg engagement vs {avg_eng_rate:.1f}% overall"
            })

        worst_type = sorted(type_avg_eng.items(), key=lambda x: x[1][0])[0]
        if worst_type[1][1] >= 5 and worst_type[1][0] < avg_eng_rate * 0.8:
            do_less.append({
                'action': f'Reduce {worst_type[0]} posts',
                'why': f'{worst_type[0]} posts averaged {worst_type[1][0]:.1f}% vs {avg_eng_rate:.1f}% overall',
                'data': f"{worst_type[1][1]} posts at {worst_type[1][0]:.1f}% engagement"
            })

    # Book-based insight: below 3000 followers, commenting is the growth engine
    if reply_count / len(posts) > 0.8 and follower_count < 20:
        do_differently.append({
            'action': 'Your reply strategy is correct for your follower stage',
            'why': 'Below 3000 followers, commenting drives most organic growth',
            'data': f"{reply_count}/{len(posts)} posts are replies. Keep commenting on creator posts in your niche."
        })

    # Original content hook advice
    if original_posts and hook_performance:
        best_hook = sorted(hook_performance.items(), key=lambda x: x[1]['avg_engagement'], reverse=True)
        if best_hook and best_hook[0][1]['count'] >= 3:
            hook_name = best_hook[0][0]
            do_differently.append({
                'action': f'When posting original content, open with a {hook_name} hook',
                'why': f'{hook_name} hooks on your original posts average {best_hook[0][1]["avg_engagement"]:.1f}% engagement',
                'data': f"Based on {best_hook[0][1]['count']} original posts with {hook_name} hooks"
            })

    # Best day
    if best_days:
        do_differently.append({
            'action': f'Post your best original content on {best_days[0]["day"]}',
            'why': f'{best_days[0]["day"]} has highest avg impressions ({best_days[0]["avg_impressions"]:.0f})',
            'data': f"Schedule high-effort original posts on this day"
        })

    # Summary
    top_ct = best_types[0][0] if best_types and best_types[0][1][1] >= 5 else 'reply'
    summary = f"Your {len(posts)} posts averaged {avg_impressions:.0f} impressions and {avg_eng_rate:.1f}% engagement. {top_ct.capitalize()} content performs best. Your reply strategy is correct at your follower stage — focus on comment quality, not volume."

    account_handle = "@user"
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            first_row = next(csv.DictReader(f))
            link = first_row.get('Post Link', '')
            if link and ('twitter.com/' in link or 'x.com/' in link):
                parts = link.split('twitter.com/') if 'twitter.com/' in link else link.split('x.com/')
                handle = parts[1].split('/')[0].replace('@', '')
                if handle:
                    account_handle = f"@{handle}"
    except:
        pass

    data = {
        'account_handle': account_handle,
        'date_range': {
            'start': date_range[0].strftime('%Y-%m-%d') if date_range[0] else '',
            'end': date_range[1].strftime('%Y-%m-%d') if date_range[1] else ''
        },
        'total_posts': len(posts),
        'overall_averages': {
            'impressions_per_post': round(avg_impressions, 0),
            'engagement_rate': round(avg_eng_rate, 2),
            'new_followers_per_post': round(avg_new_followers, 1)
        },
        'growth_funnel': {
            'profile_click_rate': round(profile_click_rate, 2),
            'follower_conversion_rate': round(follower_conversion, 3)
        },
        'top_posts': {
            'by_impressions': [
                {'text': p['text'][:120], 'impressions': p['impressions'], 'engagement_rate': round(p['eng_rate'], 1), 'new_followers': p['new_followers'], 'content_type': p['content_type'], 'hook_type': p['hook_type'], 'note': 'high reach post'} for p in by_impressions
            ],
            'by_engagement': [
                {'text': p['text'][:120], 'impressions': p['impressions'], 'engagement_rate': round(p['eng_rate'], 1), 'new_followers': p['new_followers'], 'content_type': p['content_type'], 'hook_type': p['hook_type'], 'note': 'high engagement post'} for p in by_eng_rate
            ],
            'by_followers': [
                {'text': p['text'][:120], 'impressions': p['impressions'], 'engagement_rate': round(p['eng_rate'], 1), 'new_followers': p['new_followers'], 'content_type': p['content_type'], 'hook_type': p['hook_type'], 'note': 'follower converting post'} for p in by_followers
            ]
        },
        'content_performance': content_performance,
        'best_days': best_days[:5],
        'flopped_posts': [
            {'text': p['text'][:120], 'impressions': p['impressions'], 'engagement_rate': round(p['eng_rate'], 1), 'hook_type': p['hook_type'], 'issue': 'high impressions but low engagement'} for p in flopped
        ],
        'hook_analysis': {
            'strong_hooks': strong_hooks,
            'weak_hooks': weak_hooks,
            'recommendation': hook_recommendation
        },
        'do_more': do_more,
        'do_less': do_less,
        'do_differently': do_differently,
        'summary': summary
    }

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Analysis complete: {len(posts)} posts analyzed -> {output_path}")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
