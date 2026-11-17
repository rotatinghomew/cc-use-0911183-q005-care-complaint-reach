def open_followups(store):
    values = []
    for row in store.all('reports'):
        if row['status'] == 'open' and row.get('contact'):
            values.append({'report': row['id'], 'contact': row['contact'], 'kind': 'issue_followup'})
    return values


def close_report(store, key):
    row = store.get('reports', key)
    row['status'] = 'closed'
    store.put('reports', row)
    return row


def record_reply(store, row):
    if row['result'] not in ['answered', 'refused', 'unreachable']:
        raise ValueError('回访结果不合法')
    if row['purpose'] not in ['issue_followup', 'coverage_survey']:
        raise ValueError('回访目的不合法')
    store.get('population', row['person'])
    return store.put('replies', row)
