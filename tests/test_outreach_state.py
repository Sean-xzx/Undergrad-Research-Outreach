"""Business invariants using fictional, frozen source evidence; no live model claims."""
from pathlib import Path
import json
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'undergrad-research-outreach/scripts'))
import outreach_state as engine


def source(sid='s'):
    return {'id': sid, 'url': 'https://example.org/frozen-fixture', 'observed_at': '2026-10-12T00:00:00Z',
            'access': 'retrieved', 'read_scope': 'fictional fixture body', 'excerpt': 'Frozen test evidence'}


def claim(cid, subject, predicate, value, status='supported'):
    return {'id': cid, 'subject_id': subject, 'predicate': predicate, 'value': value, 'status': status,
            'evidence': [{'source_id': 's', 'locator': 'fixture section ' + predicate, 'relation': 'supports'}]}


def base():
    return {'entities': [{'id': 'u', 'type': 'institution', 'name': 'Fictional University'},
                         {'id': 'r', 'type': 'researcher', 'name': 'Same Name', 'institution_id': 'u'}],
            'sources': [source()],
            'claims': [claim('identity', 'r', 'current_identity', 'current faculty'),
                       claim('research', 'r', 'research_category', 'joint_world_action'),
                       claim('channel', 'r', 'contact_channel', 'https://example.org/apply')],
            'constraints': [{'id': 'annual', 'predicate': 'annual_ccf_ab_count', 'operator': 'ge',
                             'value': {'year': 2026, 'catalog': 'fixture-v1', 'minimum': 4},
                             'kind': 'hard', 'scope': 'all', 'origin': 'fixture user request'}]}


def paper_batch(pid, status='formal_accepted', category='A', evidence=True):
    p = {'id': pid, 'author_ids': ['r'], 'year': 2026, 'status': status, 'paper_type': 'full',
         'ccf_category': category, 'ccf_catalog': 'fixture-v1', 'evidence': {}}
    claims = []
    if evidence:
        for field in ('author_ids', 'year', 'status', 'paper_type', 'ccf_category', 'ccf_catalog'):
            cid = pid + '-' + field
            claims.append(claim(cid, pid, field, p[field]))
            p['evidence'][field] = cid
    return {'entities': [{'id': pid, 'type': 'paper', 'name': 'Fictional paper ' + pid}],
            'claims': claims, 'papers': [p]}


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name)/'state.sqlite3'
        self.db = engine.connect(self.path)
        engine.ingest(self.db, base())

    def tearDown(self):
        self.db.close()
        self.temp.cleanup()

    def candidate(self):
        return engine.evaluate(self.db)['candidates'][0]

    def annual(self):
        return self.candidate()['conditions'][0]

    def test_narrative_cannot_count_as_papers(self):
        engine.ingest(self.db, {'claims': [claim('narrative', 'r', 'annual_news', '尚未达到数量门槛，团队声称6篇')]})
        self.assertEqual(self.annual()['status'], 'UNKNOWN')
        self.assertEqual(self.annual()['verified_lower_bound'], 0)

    def test_four_verified_papers_pass(self):
        for i in range(4):
            engine.ingest(self.db, paper_batch(f'p{i}'))
        self.assertTrue(self.candidate()['public_conditions_met'])
        self.assertEqual(self.annual()['verified_lower_bound'], 4)

    def test_duplicate_version_id_does_not_increment(self):
        engine.ingest(self.db, paper_batch('p'))
        engine.ingest(self.db, paper_batch('p', 'formal_published'))
        self.assertEqual(self.annual()['verified_lower_bound'], 1)

    def test_three_formal_two_preprints_is_unknown(self):
        for i in range(5):
            engine.ingest(self.db, paper_batch(f'p{i}', 'formal_accepted' if i < 3 else 'preprint_only'))
        self.assertEqual(self.annual()['verified_lower_bound'], 3)
        self.assertEqual(self.annual()['status'], 'UNKNOWN')

    def test_missing_evidence_does_not_count(self):
        engine.ingest(self.db, paper_batch('p', evidence=False))
        self.assertEqual(self.annual()['verified_lower_bound'], 0)

    def test_unknown_ccf_does_not_count(self):
        engine.ingest(self.db, paper_batch('p', category='unknown'))
        self.assertEqual(self.annual()['verified_lower_bound'], 0)

    def test_workshop_does_not_count(self):
        batch = paper_batch('p')
        batch['papers'][0]['paper_type'] = 'workshop'
        next(c for c in batch['claims'] if c['predicate'] == 'paper_type')['value'] = 'workshop'
        engine.ingest(self.db, batch)
        self.assertEqual(self.annual()['verified_lower_bound'], 0)

    def test_author_evidence_mismatch_rolls_back(self):
        batch = paper_batch('p')
        next(c for c in batch['claims'] if c['predicate'] == 'author_ids')['value'] = ['other']
        before = engine.snapshot(self.db)
        with self.assertRaises(ValueError):
            engine.ingest(self.db, batch)
        self.assertEqual(engine.snapshot(self.db), before)
        self.assertNotIn('p', engine.records(self.db)['entities'])

    def test_same_name_entities_stay_distinct(self):
        engine.ingest(self.db, {'entities': [{'id': 'other', 'type': 'researcher', 'name': 'Same Name'}]})
        self.assertEqual(len(engine.evaluate(self.db)['candidates']), 2)

    def test_unknown_is_not_public_match_but_allows_inquiry(self):
        self.assertFalse(self.candidate()['public_conditions_met'])
        self.assertTrue(self.candidate()['can_inquire'])

    def test_ra_does_not_imply_external_undergraduate_remote(self):
        engine.ingest(self.db, {'claims': [claim('ra', 'r', 'recruits_ra', True)],
                               'constraints': [{'id': 'remote', 'predicate': 'remote', 'operator': 'eq', 'value': True,
                                                'kind': 'hard', 'scope': 'all', 'origin': 'fixture user'}]})
        self.assertEqual(next(c for c in self.candidate()['conditions'] if c['id'] == 'remote')['status'], 'UNKNOWN')

    def test_scoped_exception_does_not_relax_others(self):
        engine.ingest(self.db, {'entities': [{'id': 'other', 'type': 'researcher', 'name': 'Other'}],
                               'constraints': [{'id': 'tier', 'predicate': 'school_tier', 'operator': 'eq', 'value': 'required',
                                                'kind': 'hard', 'scope': 'all', 'origin': 'fixture user exception', 'exceptions': ['u']}]})
        rows = {r['id']: r for r in engine.evaluate(self.db)['candidates']}
        self.assertEqual(next(c for c in rows['r']['conditions'] if c['id'] == 'tier')['status'], 'NOT_APPLICABLE')
        self.assertEqual(next(c for c in rows['other']['conditions'] if c['id'] == 'tier')['status'], 'UNKNOWN')

    def test_conflicting_claims_block_inquiry(self):
        engine.ingest(self.db, {'claims': [claim('identity-other', 'r', 'current_identity', 'different identity')]})
        self.assertFalse(self.candidate()['can_inquire'])

    def test_supported_without_evidence_rejected(self):
        item = claim('bad', 'r', 'remote', True)
        item['evidence'] = []
        with self.assertRaises(ValueError):
            engine.ingest(self.db, {'claims': [item]})

    def test_failed_source_not_evidence(self):
        item = source('failed')
        item['access'] = 'failed'
        c = claim('bad', 'r', 'remote', True)
        c['evidence'][0]['source_id'] = 'failed'
        with self.assertRaises(ValueError):
            engine.ingest(self.db, {'sources': [item], 'claims': [c]})

    def test_changed_source_invalidates_claims(self):
        changed = source()
        changed['excerpt'] = 'Changed evidence'
        engine.ingest(self.db, {'sources': [changed]})
        self.assertFalse(self.candidate()['research_candidate'])
        self.assertEqual(engine.records(self.db)['claims']['identity']['status'], 'pending')

    def test_idempotent_ingest_does_not_grow_history(self):
        before = engine.snapshot(self.db)
        self.assertEqual(engine.ingest(self.db, base())['changed'], 0)
        self.assertEqual(engine.snapshot(self.db), before)

    def test_contact_events_survive_candidate_import(self):
        event = {'id': 'sent', 'subject_id': 'r', 'type': 'sent_confirmed',
                 'occurred_at': '2026-10-12T01:00:00Z', 'basis': 'fictional user confirmation'}
        engine.ingest(self.db, {'events': [event]})
        engine.ingest(self.db, base())
        self.assertEqual(self.candidate()['contact_state'], 'sent_confirmed')

    def test_contact_event_cannot_be_overwritten(self):
        event = {'id': 'sent', 'subject_id': 'r', 'type': 'sent_confirmed',
                 'occurred_at': '2026-10-12T01:00:00Z', 'basis': 'fictional user confirmation'}
        engine.ingest(self.db, {'events': [event]})
        event['type'] = 'send_result_unknown'
        with self.assertRaises(ValueError):
            engine.ingest(self.db, {'events': [event]})

    def test_resume_recovers_interrupted_task(self):
        engine.ingest(self.db, {'tasks': [{'id': 't', 'kind': 'coverage', 'target_id': 'u',
                                         'state': 'running', 'reason': 'missing coverage', 'path': 'institution'}]})
        result = engine.resume(self.db)
        self.assertEqual(result['next_tasks'][0]['state'], 'retryable')
        self.assertFalse(result['report']['scope_complete'])

    def test_blocked_coverage_is_not_complete(self):
        engine.ingest(self.db, {'tasks': [{'id': 't', 'kind': 'coverage', 'target_id': 'u',
                                         'state': 'blocked', 'reason': 'access restricted', 'path': 'institution'}]})
        self.assertFalse(engine.evaluate(self.db)['scope_complete'])

    def test_tasks_wait_for_dependencies(self):
        engine.ingest(self.db, {'tasks': [
            {'id': 'a', 'kind': 'coverage', 'target_id': 'u', 'state': 'pending', 'reason': 'coverage', 'path': 'institution'},
            {'id': 'b', 'kind': 'verify', 'target_id': 'r', 'state': 'pending', 'reason': 'verify', 'path': 'paper', 'depends_on': ['a']}]})
        self.assertEqual([t['id'] for t in engine.next_tasks(self.db)], ['a'])

    def test_legacy_import_preserves_payload_without_verifying(self):
        row = {'name': 'Legacy', 'school': 'Legacy institution', 'home': 'https://example.org/legacy',
               'threshold': '数量门槛有依据', 'status': '已发', 'other': 'old source'}
        engine.import_legacy(self.db, [row])
        e = next(e for e in engine.records(self.db)['entities'].values() if e.get('legacy'))
        self.assertEqual(e['legacy'], row)
        report = next(r for r in engine.evaluate(self.db)['candidates'] if r['id'] == e['id'])
        self.assertFalse(report['research_candidate'])
        self.assertEqual(report['contact_state'], 'not_contacted')
        self.assertEqual(engine.import_legacy(self.db, [row])['changed'], 0)

    def test_reopen_keeps_committed_events(self):
        event = {'id': 'reply', 'subject_id': 'r', 'type': 'reply_received',
                 'occurred_at': '2026-10-12T01:00:00Z', 'basis': 'fictional received reply'}
        engine.ingest(self.db, {'events': [event]})
        self.db.close()
        self.db = engine.connect(self.path)
        self.assertEqual(self.candidate()['contact_state'], 'reply_received')

    def test_unknown_fields_are_rejected(self):
        c = claim('bad', 'r', 'remote', True)
        c['guaranteed'] = True
        with self.assertRaises(ValueError):
            engine.ingest(self.db, {'claims': [c]})

    def test_dependency_cycle_rejected_atomically(self):
        before = engine.snapshot(self.db)
        with self.assertRaises(ValueError):
            engine.ingest(self.db, {'tasks': [
                {'id': 'a', 'kind': 'verify', 'target_id': 'r', 'state': 'pending', 'reason': 'a', 'path': 'paper', 'depends_on': ['b']},
                {'id': 'b', 'kind': 'verify', 'target_id': 'r', 'state': 'pending', 'reason': 'b', 'path': 'paper', 'depends_on': ['a']}]})
        self.assertEqual(engine.snapshot(self.db), before)

    def test_exception_to_nonexistent_entity_rejected(self):
        with self.assertRaises(ValueError):
            engine.ingest(self.db, {'constraints': [{'id': 'bad', 'predicate': 'tier', 'operator': 'eq', 'value': True,
                'kind': 'hard', 'scope': 'all', 'origin': 'fixture', 'exceptions': ['missing']}]})

    def test_timezone_required(self):
        event = {'id': 'bad', 'subject_id': 'r', 'type': 'sent_confirmed',
                 'occurred_at': '2026-10-12T01:00:00', 'basis': 'fictional confirmation'}
        with self.assertRaises(ValueError):
            engine.ingest(self.db, {'events': [event]})

    def test_stale_digest_rejected(self):
        c = claim('bad', 'r', 'remote', True)
        c['evidence'][0]['source_digest'] = 'outdated'
        with self.assertRaises(ValueError):
            engine.ingest(self.db, {'claims': [c]})

    def test_json_contract_matches_record_fields(self):
        path = Path(engine.__file__).parent/'schemas/batch.schema.json'
        definitions = json.loads(path.read_text(encoding='utf8'))['$defs']
        for kind in engine.KINDS:
            self.assertEqual(set(definitions[kind]['properties']), engine.FIELDS[kind])
            self.assertEqual(set(definitions[kind]['required']), engine.REQUIRED[kind])

    def test_new_requirement_invalidates_previous_match(self):
        for i in range(4):
            engine.ingest(self.db, paper_batch(f'p{i}'))
        self.assertTrue(self.candidate()['public_conditions_met'])
        rules = base()['constraints']
        rules[0]['value']['minimum'] = 5
        engine.ingest(self.db, {'constraints': rules})
        self.assertFalse(self.candidate()['public_conditions_met'])

    def test_entity_id_cannot_change_type(self):
        with self.assertRaises(ValueError):
            engine.ingest(self.db, {'entities': [{'id': 'r', 'type': 'institution', 'name': 'Repurposed'}]})

    def test_claim_id_cannot_change_subject(self):
        with self.assertRaises(ValueError):
            engine.ingest(self.db, {'claims': [claim('identity', 'u', 'current_identity', 'different subject')]})

    def test_other_author_papers_do_not_count(self):
        engine.ingest(self.db, {'entities': [{'id': 'other', 'type': 'researcher', 'name': 'Other'}]})
        batch = paper_batch('p')
        batch['papers'][0]['author_ids'] = ['other']
        next(c for c in batch['claims'] if c['predicate'] == 'author_ids')['value'] = ['other']
        engine.ingest(self.db, batch)
        self.assertEqual(self.annual()['verified_lower_bound'], 0)

    def test_conflicting_publication_state_does_not_count(self):
        engine.ingest(self.db, paper_batch('p'))
        engine.ingest(self.db, {'claims': [claim('p-status-conflict', 'p', 'status', 'preprint_only')]})
        self.assertEqual(self.annual()['verified_lower_bound'], 0)


if __name__ == '__main__':
    unittest.main()
