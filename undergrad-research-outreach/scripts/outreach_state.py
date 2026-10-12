"""Local evidence ledger. No network requests or external contact actions."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3

SCHEMA_VERSION = 1
KINDS = {'entities', 'sources', 'claims', 'papers', 'constraints', 'tasks', 'events'}
CLAIM_STATES = {'pending', 'supported', 'contradicted', 'conflict', 'superseded'}
TASK_STATES = {'pending', 'running', 'done', 'retryable', 'blocked', 'cancelled'}
EVENT_TYPES = {'legacy_imported', 'draft_created', 'send_authorized', 'sent_confirmed',
               'send_result_unknown', 'reply_received', 'declined', 'paused',
               'arrangement_confirmed', 'correction_recorded'}
FIELDS = {
    'entities': {'id', 'type', 'name', 'aliases', 'institution_id', 'legacy'},
    'sources': {'id', 'url', 'observed_at', 'page_date', 'access', 'excerpt', 'read_scope'},
    'claims': {'id', 'subject_id', 'predicate', 'value', 'status', 'evidence', 'reason'},
    'papers': {'id', 'author_ids', 'year', 'status', 'paper_type', 'ccf_category', 'ccf_catalog', 'evidence'},
    'constraints': {'id', 'predicate', 'operator', 'value', 'kind', 'scope', 'origin', 'exceptions'},
    'tasks': {'id', 'kind', 'target_id', 'state', 'reason', 'path', 'depends_on', 'attempts'},
    'events': {'id', 'subject_id', 'type', 'occurred_at', 'basis', 'payload'},
}
REQUIRED = {
    'entities': {'id', 'type', 'name'},
    'sources': {'id', 'url', 'observed_at', 'access', 'read_scope'},
    'claims': {'id', 'subject_id', 'predicate', 'value', 'status', 'evidence'},
    'papers': {'id', 'author_ids', 'year', 'status', 'paper_type', 'ccf_category', 'ccf_catalog', 'evidence'},
    'constraints': {'id', 'predicate', 'operator', 'value', 'kind', 'scope', 'origin'},
    'tasks': {'id', 'kind', 'target_id', 'state', 'reason', 'path'},
    'events': {'id', 'subject_id', 'type', 'occurred_at', 'basis'},
}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode('utf8')).hexdigest()


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def connect(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.execute('PRAGMA foreign_keys=ON')
    db.executescript('''
        CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS records (
          kind TEXT NOT NULL, id TEXT NOT NULL, body TEXT NOT NULL,
          revision INTEGER NOT NULL, PRIMARY KEY(kind,id));
        CREATE TABLE IF NOT EXISTS history (
          sequence INTEGER PRIMARY KEY, kind TEXT NOT NULL, id TEXT NOT NULL,
          body TEXT NOT NULL, revision INTEGER NOT NULL, changed_at TEXT NOT NULL);
    ''')
    row = db.execute("SELECT value FROM metadata WHERE key='schema_version'").fetchone()
    if row and int(row[0]) != SCHEMA_VERSION:
        db.close()
        raise ValueError('Unsupported database schema; preserve the database and migrate explicitly')
    db.execute("INSERT OR IGNORE INTO metadata VALUES ('schema_version',?)", (str(SCHEMA_VERSION),))
    db.commit()
    return db


def records(db):
    result = {k: {} for k in KINDS}
    for kind, rid, body in db.execute('SELECT kind,id,body FROM records'):
        result[kind][rid] = json.loads(body)
    return result


def validate_shape(kind, item):
    if not isinstance(item, dict) or not REQUIRED[kind] <= item.keys():
        raise ValueError(f'{kind}: missing required fields')
    if set(item) - FIELDS[kind]:
        raise ValueError(f'{kind}: unknown fields {sorted(set(item)-FIELDS[kind])}')
    if not isinstance(item['id'], str) or not item['id'].strip():
        raise ValueError('Record id must be a nonempty stable string')
    nonscalar = {'value', 'legacy', 'payload', 'author_ids', 'aliases', 'depends_on', 'exceptions', 'evidence', 'year', 'attempts'}
    if any(not isinstance(item[f], str) for f in item.keys() - nonscalar):
        raise ValueError('Scalar contract fields must be strings')
    for field in {'subject_id', 'predicate', 'kind', 'scope', 'origin', 'reason', 'path', 'target_id', 'name', 'type', 'basis', 'ccf_catalog'} & item.keys():
        if not isinstance(item[field], str) or not item[field].strip():
            raise ValueError(f'{field} must be a nonempty string')
    for field in {'author_ids', 'aliases', 'depends_on', 'exceptions'} & item.keys():
        if not isinstance(item[field], list) or any(not isinstance(v, str) or not v for v in item[field]):
            raise ValueError(f'{field} must be an array of nonempty strings')
    if 'legacy' in item and not isinstance(item['legacy'], dict):
        raise ValueError('Legacy payload must be an object')
    if kind == 'entities' and item['type'] not in {'researcher', 'institution', 'project', 'paper'}:
        raise ValueError('Invalid entity type')
    if kind == 'sources':
        if not isinstance(item['url'], str) or not item['url'].startswith(('https://', 'http://')):
            raise ValueError('Source must have an HTTP(S) URL')
        if item['access'] not in {'retrieved', 'restricted', 'failed'} or not item['read_scope']:
            raise ValueError('Invalid source access/read scope')
        if not datetime.fromisoformat(item['observed_at'].replace('Z', '+00:00')).tzinfo:
            raise ValueError('Source timestamp must contain a timezone')
    if kind == 'claims':
        if item['status'] not in CLAIM_STATES or not isinstance(item['evidence'], list):
            raise ValueError('Invalid claim state/evidence')
    if kind == 'papers':
        if type(item['year']) is not int or not 1900 <= item['year'] <= 2200:
            raise ValueError('Paper year must be an integer')
        if not isinstance(item['author_ids'], list) or len(set(item['author_ids'])) != len(item['author_ids']):
            raise ValueError('Authors must be distinct entity ids')
        if item['status'] not in {'formal_accepted', 'formal_published', 'preprint_only', 'unknown'}:
            raise ValueError('Invalid publication status')
        if item['paper_type'] not in {'full', 'workshop', 'other'}:
            raise ValueError('Invalid paper type')
        if item['ccf_category'] not in {'A', 'B', 'C', 'unlisted', 'unknown'} or not isinstance(item['evidence'], dict):
            raise ValueError('Invalid CCF category or field evidence')
    if kind == 'constraints':
        if item['kind'] not in {'hard', 'preference'} or item['operator'] not in {'eq', 'in', 'ge'}:
            raise ValueError('Invalid constraint kind/operator')
        if not item['origin'] or not item['scope']:
            raise ValueError('Constraint requires user origin and explicit scope')
        if item['operator'] == 'in' and not isinstance(item['value'], list):
            raise ValueError('in requires a list')
        if item['predicate'] == 'annual_ccf_ab_count':
            v = item['value']
            if item['operator'] != 'ge' or not isinstance(v, dict) or set(v) != {'year', 'catalog', 'minimum'}:
                raise ValueError('Annual constraint requires year/catalog/minimum')
            if type(v['year']) is not int or type(v['minimum']) is not int or v['minimum'] < 0 or not v['catalog']:
                raise ValueError('Invalid annual output policy')
    if kind == 'tasks' and (item['state'] not in TASK_STATES or type(item.get('attempts', 0)) is not int or item.get('attempts', 0) < 0):
        raise ValueError('Invalid task state/attempt count')
    if kind == 'events':
        if item['type'] not in EVENT_TYPES or not item['basis']:
            raise ValueError('Event requires a supported type and real basis')
        if not datetime.fromisoformat(item['occurred_at'].replace('Z', '+00:00')).tzinfo:
            raise ValueError('Event timestamp must contain a timezone')


def ingest(db, batch):
    """Validate the entire input, then atomically commit; repeated input is a no-op."""
    if not isinstance(batch, dict) or set(batch) - KINDS:
        raise ValueError('Unknown batch record kind')
    state = records(db)
    incoming = []
    for kind, items in batch.items():
        if not isinstance(items, list):
            raise ValueError('Batch sections must be arrays')
        ids = set()
        for raw in items:
            validate_shape(kind, raw)
            if raw['id'] in ids:
                raise ValueError('Duplicate id in one batch')
            ids.add(raw['id'])
            item = json.loads(canonical(raw))
            previous = state[kind].get(item['id'])
            if kind == 'entities' and previous and previous['type'] != item['type']:
                raise ValueError('Entity type is stable; resolve identity explicitly')
            if kind == 'claims' and previous and (previous['subject_id'], previous['predicate']) != (item['subject_id'], item['predicate']):
                raise ValueError('Claim id cannot be repurposed for another fact')
            if kind == 'events' and item['id'] in state[kind] and state[kind][item['id']] != item:
                raise ValueError('Events are immutable; append a correction event')
            state[kind][item['id']] = item
            incoming.append((kind, item))
    for kind, item in incoming:
        if kind == 'claims':
            if item['subject_id'] not in state['entities']:
                raise ValueError('Claim subject is missing')
            supports, contradicts = False, False
            for evidence in item['evidence']:
                if not isinstance(evidence, dict):
                    raise ValueError('Evidence must be an object')
                if any(not isinstance(evidence.get(f), str) or not evidence[f] for f in ('source_id', 'locator', 'relation')):
                    raise ValueError('Evidence source, locator and relation must be nonempty strings')
                if set(evidence) - {'source_id', 'locator', 'relation', 'source_digest'}:
                    raise ValueError('Unknown evidence fields')
                source = state['sources'].get(evidence.get('source_id'))
                if not source or source['access'] != 'retrieved' or not evidence.get('locator'):
                    raise ValueError('Evidence needs a retrieved source and readable locator')
                if evidence.get('relation') not in {'supports', 'contradicts'}:
                    raise ValueError('Invalid evidence relation')
                supports |= evidence['relation'] == 'supports'
                contradicts |= evidence['relation'] == 'contradicts'
                expected = digest(source)
                if evidence.get('source_digest', expected) != expected:
                    raise ValueError('Evidence refers to a stale source')
                evidence['source_digest'] = expected
            if item['status'] == 'supported' and (not supports or contradicts):
                raise ValueError('Supported claims require support without unresolved contradiction')
        if kind == 'entities' and item.get('institution_id'):
            institution = state['entities'].get(item['institution_id'])
            if not institution or institution['type'] != 'institution':
                raise ValueError('Institution reference is missing')
        if kind == 'papers':
            if item['id'] not in state['entities'] or state['entities'][item['id']]['type'] != 'paper':
                raise ValueError('Paper needs a paper entity')
            for author in item['author_ids']:
                if author not in state['entities'] or state['entities'][author]['type'] != 'researcher':
                    raise ValueError('Author must be a researcher entity')
            for field, claim_id in item['evidence'].items():
                claim = state['claims'].get(claim_id)
                if field not in {'author_ids', 'year', 'status', 'paper_type', 'ccf_category', 'ccf_catalog'}:
                    raise ValueError('Unknown paper evidence field')
                if not claim or claim['subject_id'] != item['id'] or claim['predicate'] != field or claim['value'] != item[field]:
                    raise ValueError('Paper field evidence does not match the paper')
        if kind == 'events' and item['subject_id'] not in state['entities']:
            raise ValueError('Event subject is missing')
        if kind == 'tasks':
            if item['target_id'] not in state['entities']:
                raise ValueError('Task target is missing')
            for dep in item.get('depends_on', []):
                if dep not in state['tasks'] or dep == item['id']:
                    raise ValueError('Task dependency is missing or self-referencing')
        if kind == 'constraints':
            if item['scope'] != 'all' and item['scope'] not in state['entities']:
                raise ValueError('Constraint scope entity is missing')
            if any(e not in state['entities'] for e in item.get('exceptions', [])):
                raise ValueError('Exception must target an existing entity')
    visiting, visited = set(), set()
    def visit(tid):
        if tid in visiting:
            raise ValueError('Task dependency cycle')
        if tid in visited:
            return
        visiting.add(tid)
        for dep in state['tasks'][tid].get('depends_on', []):
            visit(dep)
        visiting.remove(tid)
        visited.add(tid)
    for tid in state['tasks']:
        visit(tid)
    # Any changed source invalidates old supported claims, unless reverified in this batch.
    refreshed = {i['id'] for k, i in incoming if k == 'claims'}
    for claim in state['claims'].values():
        if claim['id'] in refreshed or claim['status'] != 'supported':
            continue
        if any(e.get('source_digest') != digest(state['sources'][e['source_id']]) for e in claim['evidence']):
            claim['status'] = 'pending'
            claim['reason'] = 'source_changed; reverify before using the conclusion'
            incoming.append(('claims', claim))
    changed = 0
    with db:
        for kind, item in incoming:
            body = canonical(item)
            old = db.execute('SELECT body,revision FROM records WHERE kind=? AND id=?', (kind, item['id'])).fetchone()
            if old and old[0] == body:
                continue
            rev = old[1] + 1 if old else 1
            db.execute('INSERT INTO history(kind,id,body,revision,changed_at) VALUES (?,?,?,?,?)',
                       (kind, item['id'], body, rev, timestamp()))
            db.execute('INSERT INTO records VALUES (?,?,?,?) ON CONFLICT(kind,id) DO UPDATE SET body=excluded.body,revision=excluded.revision',
                       (kind, item['id'], body, rev))
            changed += 1
    return {'changed': changed, 'snapshot': snapshot(db)}


def snapshot(db):
    return db.execute('SELECT COALESCE(MAX(sequence),0) FROM history').fetchone()[0]


def claims_for(state, subject, predicate):
    return [c for c in state['claims'].values() if c['subject_id'] == subject
            and c['predicate'] == predicate and c['status'] != 'superseded']


def conclusion(state, subject, predicate):
    items = claims_for(state, subject, predicate)
    supported = [c for c in items if c['status'] == 'supported']
    if any(c['status'] in {'conflict', 'contradicted'} for c in items):
        return 'CONFLICT', None, [c['id'] for c in items]
    values = {canonical(c['value']) for c in supported}
    if len(values) > 1:
        return 'CONFLICT', None, [c['id'] for c in supported]
    if not supported:
        return 'UNKNOWN', None, [c['id'] for c in items]
    return 'PASS', supported[0]['value'], [c['id'] for c in supported]


def paper_verified(state, paper):
    fields = {'author_ids', 'year', 'status', 'paper_type', 'ccf_category', 'ccf_catalog'}
    if set(paper['evidence']) != fields:
        return False
    return all(conclusion(state, paper['id'], field)[:2] == ('PASS', paper[field]) for field in fields)


def annual_count(state, researcher, policy):
    verified = [p['id'] for p in state['papers'].values()
                if researcher in p['author_ids'] and p['year'] == policy['year']
                and p['ccf_catalog'] == policy['catalog'] and p['ccf_category'] in {'A', 'B'}
                and p['status'] in {'formal_accepted', 'formal_published'} and p['paper_type'] == 'full'
                and paper_verified(state, p)]
    count = len(verified)
    return {'status': 'PASS' if count >= policy['minimum'] else 'UNKNOWN',
            'verified_lower_bound': count, 'paper_ids': verified,
            'reason': 'minimum_verified' if count >= policy['minimum'] else 'incomplete_list_is_not_low_output'}


def contact_state(state, subject):
    events = sorted([e for e in state['events'].values() if e['subject_id'] == subject],
                    key=lambda e: (datetime.fromisoformat(e['occurred_at'].replace('Z', '+00:00')), e['id']))
    relevant = [e for e in events if e['type'] in {'sent_confirmed', 'send_result_unknown', 'reply_received',
                                                  'declined', 'paused', 'arrangement_confirmed'}]
    return relevant[-1]['type'] if relevant else 'not_contacted'


def evaluate(db):
    state = records(db)
    candidates = []
    for entity in state['entities'].values():
        if entity['type'] != 'researcher':
            continue
        rid = entity['id']
        conditions = []
        for rule in state['constraints'].values():
            if rule['scope'] not in {'all', rid, entity.get('institution_id')}:
                continue
            if rid in rule.get('exceptions', []) or entity.get('institution_id') in rule.get('exceptions', []):
                conditions.append({'id': rule['id'], 'kind': rule['kind'], 'status': 'NOT_APPLICABLE', 'reason': 'explicit_user_exception'})
                continue
            if rule['predicate'] == 'annual_ccf_ab_count':
                result = annual_count(state, rid, rule['value'])
            else:
                status, value, evidence = conclusion(state, rid, rule['predicate'])
                passed = False
                if status == 'PASS':
                    if rule['operator'] == 'eq':
                        passed = value == rule['value']
                    elif rule['operator'] == 'in':
                        passed = value in rule['value']
                    elif rule['operator'] == 'ge':
                        passed = type(value) in {int, float} and type(rule['value']) in {int, float} and value >= rule['value']
                    status = 'PASS' if passed else 'FAIL'
                result = {'status': status, 'claim_ids': evidence}
            conditions.append({'id': rule['id'], 'kind': rule['kind'], **result})
        identity = conclusion(state, rid, 'current_identity')
        research = conclusion(state, rid, 'research_category')
        channel = conclusion(state, rid, 'contact_channel')
        base = identity[0] == 'PASS' and bool(identity[1]) and research[0] == 'PASS' and bool(research[1])
        hard = [c for c in conditions if c['kind'] == 'hard']
        no_fail = not any(c['status'] in {'FAIL', 'CONFLICT'} for c in hard)
        inquire = base and channel[0] == 'PASS' and bool(channel[1]) and no_fail
        meets = base and bool(hard) and all(c['status'] in {'PASS', 'NOT_APPLICABLE'} for c in hard)
        candidates.append({'id': rid, 'name': entity['name'], 'research_candidate': base,
                           'research_category': research[1], 'can_inquire': inquire,
                           'public_conditions_met': meets, 'conditions': conditions,
                           'contact_state': contact_state(state, rid)})
    coverage = [t for t in state['tasks'].values() if t['kind'] == 'coverage']
    return {'schema_version': SCHEMA_VERSION, 'snapshot': snapshot(db), 'candidates': candidates,
            'coverage': coverage, 'scope_complete': bool(coverage) and all(t['state'] in {'done', 'cancelled'} for t in coverage)}


def next_tasks(db):
    state = records(db)
    order = {'identity_conflict': 0, 'coverage': 1, 'verify': 2, 'discover': 3}
    eligible = [t for t in state['tasks'].values() if t['state'] in {'pending', 'retryable'}
                and all(state['tasks'][d]['state'] == 'done' for d in t.get('depends_on', []))]
    return sorted(eligible, key=lambda t: (order.get(t['kind'], 4), t.get('attempts', 0), t['id']))


def resume(db):
    state = records(db)
    interrupted = [dict(t, state='retryable', reason=t['reason'] + '; interrupted; check committed evidence')
                   for t in state['tasks'].values() if t['state'] == 'running']
    if interrupted:
        ingest(db, {'tasks': interrupted})
    return {'snapshot': snapshot(db), 'constraints': list(records(db)['constraints'].values()),
            'next_tasks': next_tasks(db), 'report': evaluate(db)}


def import_legacy(db, rows):
    """Preserve originals without turning narrative conclusions into verified facts."""
    batch = {'entities': [], 'events': []}
    existing = records(db)
    for row in rows:
        institution = 'legacy-institution-' + digest(row['school'])[:16]
        researcher = 'legacy-researcher-' + digest([row['school'], row['name'], row.get('home')])[:16]
        if not any(e['id'] == institution for e in batch['entities']):
            batch['entities'].append({'id': institution, 'type': 'institution', 'name': row['school']})
        batch['entities'].append({'id': researcher, 'type': 'researcher', 'name': row['name'],
                                  'institution_id': institution, 'legacy': row})
        event_id = 'import-' + digest(row)
        batch['events'].append({'id': event_id, 'subject_id': researcher, 'type': 'legacy_imported',
                                'occurred_at': existing['events'].get(event_id, {}).get('occurred_at', timestamp()),
                                'basis': 'original local record; not an independently verified contact event',
                                'payload': {'original_status': row.get('status'), 'data_digest': digest(row)}})
    return ingest(db, batch)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', type=Path, required=True)
    parser.add_argument('command', choices=['init', 'ingest', 'evaluate', 'next-tasks', 'resume', 'export-view', 'import-legacy'])
    parser.add_argument('--input', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        with connect(args.db) as db:
            if args.command in {'ingest', 'import-legacy'}:
                if not args.input:
                    raise ValueError('--input is required')
                value = json.loads(args.input.read_text(encoding='utf8'))
                result = ingest(db, value) if args.command == 'ingest' else import_legacy(db, value)
            elif args.command == 'next-tasks':
                result = next_tasks(db)
            elif args.command == 'resume':
                result = resume(db)
            elif args.command == 'init':
                result = {'schema_version': SCHEMA_VERSION, 'snapshot': snapshot(db)}
            else:
                result = evaluate(db)
            text = json.dumps(result, ensure_ascii=False, indent=2)
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                temporary = args.output.with_name(args.output.name + '.tmp')
                temporary.write_text(text, encoding='utf8')
                temporary.replace(args.output)
            else:
                print(text)
    except (ValueError, KeyError, TypeError, OSError, sqlite3.Error) as error:
        parser.exit(1, f'FAIL: {error}\n')


if __name__ == '__main__':
    main()
