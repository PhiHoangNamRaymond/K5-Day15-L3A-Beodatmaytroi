"""Local draft persistence. Source spreadsheets remain immutable."""
import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = Path(os.environ.get('SCHEDULE_DB', ROOT / '.local/schedule.sqlite3'))


@contextmanager
def connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB, timeout=15)
    try:
        with db:
            db.execute('CREATE TABLE IF NOT EXISTS records (kind TEXT, key TEXT, body TEXT, PRIMARY KEY(kind,key))')
            yield db
    finally:
        db.close()


def get(kind, key, default=None):
    with connect() as db:
        row = db.execute('SELECT body FROM records WHERE kind=? AND key=?', (kind, key)).fetchone()
    return json.loads(row[0]) if row else default


def put(kind, key, body):
    with connect() as db:
        db.execute('INSERT OR REPLACE INTO records VALUES (?,?,?)', (kind, key, json.dumps(body, ensure_ascii=False)))
    return body


def stamp():
    return datetime.now(timezone.utc).isoformat()


def draft_key(week, fingerprint):
    return fingerprint + ':' + week


def save_draft(draft, fingerprint):
    return put('draft', draft_key(draft['week'], fingerprint), dict(draft, saved_at=stamp()))


def handoff(week, rows, notice, fingerprint):
    record = {'approved': True, 'week': week, 'rows': rows, 'notice': notice,
              'approved_at': stamp(), 'fingerprint': fingerprint}
    put('handoff', draft_key(week, fingerprint), record)
    put('audit', record['approved_at'], {'action': 'approve', 'week': week, 'fingerprint': fingerprint})
    return record
