from domain.matching import AMatchRepository, Matching, Party, Entry, EntryEntity, Match, Player, EntryQuery
from sqlalchemy.orm import Session
from infra.matching import MatchRepository, EntryRepository
from uuid import uuid4
from datetime import datetime
from typing import Optional

class ProtoMatchRepository(AMatchRepository):
    pass


def query_entry(db: Session, entry_query: EntryQuery) -> list[EntryEntity]:
    return EntryRepository(db).find_by_query(entry_query)

def create_entry(db: Session, entry: EntryEntity) -> EntryEntity:
    entry.id = uuid4()
    return EntryRepository(db).save(entry)

def update_entry(db: Session, entry: EntryEntity) -> EntryEntity:
    return EntryRepository(db).save(entry)

def _closed_entry(entry: EntryEntity) -> EntryEntity:
    _entry = EntryEntity(entry.id, entry.players, entry.closed_at)
    _entry.closed_at = datetime.now()
    return _entry

def make_match(db: Session) -> Optional[Match]:
    empty_entry_query = EntryQuery(is_closed=False, has_players=False)
    empty_entries = EntryRepository(db).find_by_query(empty_entry_query)
    closed_entries = map(_closed_entry, empty_entries)
    for e in closed_entries:
        update_entry(db, e)

    entry_query = EntryQuery(is_closed=False, has_players=True)
    entry_entities = EntryRepository(db).find_by_query(entry_query)
    if not entry_entities:
        return None
    
    entries = [Entry(e.players) for e in entry_entities]
    matching = Matching(entries)
    parties = parties_from_entries(matching.make_match())
    payload = Match(uuid4(), parties)
    match = MatchRepository(db).save(payload)
    closed_entries = map(_closed_entry, entry_entities)
    for e in closed_entries:
        update_entry(db, e)

    return match


def make_match_with_new_entries(db: Session, entries: list[Entry]) -> Match:
    matching = Matching(entries)
    parties = parties_from_entries(matching.make_match())
    payload = Match(uuid4(), parties)
    return MatchRepository(db).save(payload)


def make_match_proto(db: Session, entries: list[Entry]) -> Match:
    matching = Matching(entries)
    parties = parties_from_entries(matching.make_match())
    payload = Match(uuid4(), parties)
    return ProtoMatchRepository(db).save(payload)


def parties_from_entries(entries: list[Entry]) -> list[Party]:
    return [Party(uuid4(), [Player(p.id, p.name, p.point) for p in e.players]) for e in entries]
