from .channels import explicit_groups


def observed_coverage(store):
    groups = explicit_groups(store)
    counts = {}
    for group in groups:
        pattern = '+'.join(group['channels'])
        counts[pattern] = counts.get(pattern, 0) + 1
    return {'observed_issues': len(groups), 'patterns': counts, 'interpretation': '仅为确认编号对应的已见诉求，不估计未报告数量'}


def channel_calendar(store, day):
    return {row['channel']: row['available'] for row in store.all('availability') if row['start'] <= day < row['end']}
