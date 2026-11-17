def save_report(store, row):
    if row['channel'] not in ['hotline', 'book', 'survey']:
        raise ValueError('不支持的来源渠道')
    if row.get('anonymous') and row.get('contact'):
        raise ValueError('匿名记录不能带联系标记')
    if row['status'] not in ['open', 'closed']:
        raise ValueError('问题状态不合法')
    return store.put('reports', row)


def explicit_groups(store):
    groups = {}
    for row in store.all('reports'):
        key = 'issue:' + row['issue'] if row.get('issue') else 'record:' + row['id']
        groups.setdefault(key, []).append(row)
    return [{'id': key, 'reports': sorted(row['id'] for row in rows), 'channels': sorted({row['channel'] for row in rows})} for key, rows in sorted(groups.items())]
