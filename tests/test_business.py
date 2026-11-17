import unittest
from complaints.app import Application
from complaints.store import Store
from complaints.channels import save_report, explicit_groups
from complaints.coverage import observed_coverage, channel_calendar
from complaints.followthrough import open_followups, close_report, record_reply


class ComplaintTests(unittest.TestCase):
    def setUp(self):
        self.store = Store(':memory:')
        Application(self.store).seed()

    def tearDown(self):
        self.store.close()

    def test_explicit_issue_overlap(self):
        self.assertEqual(observed_coverage(self.store)['observed_issues'], 3)

    def test_anonymous_not_merged_by_date(self):
        self.assertIn('record:a1', [row['id'] for row in explicit_groups(self.store)])

    def test_no_identity_in_anonymous_record(self):
        row = dict(self.store.get('reports', 'a1'), contact='token')
        with self.assertRaises(ValueError):
            save_report(self.store, row)

    def test_unavailable_channel_retained(self):
        self.assertFalse(channel_calendar(self.store, '2026-10-03')['book'])

    def test_calendar_end_exclusive(self):
        self.assertNotIn('book', channel_calendar(self.store, '2026-10-08'))

    def test_followup_requires_contact(self):
        self.assertEqual(len(open_followups(self.store)), 2)

    def test_close_removes_followup(self):
        close_report(self.store, 'h1')
        self.assertEqual([row['report'] for row in open_followups(self.store)], ['b1'])

    def test_unknown_channel_rejected(self):
        row = dict(self.store.get('reports', 'h1'), channel='other')
        with self.assertRaises(ValueError):
            save_report(self.store, row)

    def test_reply_preserves_purpose(self):
        row = {'id': 'x', 'person': 'p4', 'purpose': 'coverage_survey', 'result': 'answered'}
        record_reply(self.store, row)
        self.assertEqual(self.store.get('replies', 'x')['purpose'], 'coverage_survey')

    def test_unknown_reply_person(self):
        with self.assertRaises(KeyError):
            record_reply(self.store, {'id': 'x', 'person': 'missing', 'purpose': 'coverage_survey', 'result': 'answered'})
