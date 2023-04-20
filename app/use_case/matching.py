from domain.matching import AMatchRepository, Matching, Party, Entry, EntryEntity, Match, Player, EntryQuery, MatchEntryLink, split_entries
from sqlalchemy.orm import Session
from infra.matching import MatchRepository, EntryRepository, MatchEntryLinkRepository
from uuid import uuid4, UUID
from datetime import datetime
from typing import Optional, List

class ProtoMatchRepository(AMatchRepository):
    pass


def query_entry(db: Session, entry_query: EntryQuery) -> List[EntryEntity]:
    return EntryRepository(db).find_by_query(entry_query)

def create_entry(db: Session, entry: EntryEntity) -> EntryEntity:
    entry.id = uuid4()
    return EntryRepository(db).save(entry)

def update_entry(db: Session, entry: EntryEntity) -> EntryEntity:
    return EntryRepository(db).save(entry)

def _closed_entry(entry: EntryEntity, closed_at=None) -> EntryEntity:
    _entry = EntryEntity(entry.id, entry.players, entry.closed_at)
    _entry.closed_at = closed_at
    return _entry

def close_entries(db: Session, entries: List[EntryEntity], closed_at=None) -> None:
    if closed_at is None:
        closed_at = datetime.now()

    closed_entries = map(lambda e: _closed_entry(e, closed_at), entries)
    for e in closed_entries:
        update_entry(db, e)

def query_match(db: Session) -> List[Match]:
    return MatchRepository(db).find_by_query()

def fetch_match(db: Session, match_id: UUID) -> Match:
    return MatchRepository(db).find_by_id(match_id)

def make_match(db: Session) -> List[Match]:
    empty_entry_query = EntryQuery(is_closed=False, has_players=False)
    empty_entries = EntryRepository(db).find_by_query(empty_entry_query)
    close_entries(db, empty_entries)

    entry_query = EntryQuery(is_closed=False, has_players=True)
    entry_entities = EntryRepository(db).find_by_query(entry_query)
    if not entry_entities:
        return []

    
    splitted_entries = split_entries(entry_entities)
    
    matches = []
    for entries in splitted_entries:
        matching = Matching([Entry(e.players) for e in entries])
        res = matching.make_match()
        
        parties = parties_from_entries(res)
        
        payload = Match(uuid4(), parties)
        match = MatchRepository(db).save(payload)

        match_entry_link = MatchEntryLink(match.id, [e.id for e in entries])
        MatchEntryLinkRepository(db).save(match_entry_link)

        matches.append(match)

    return matches

class MatchEntryEmptyError(Exception):
    pass

def commit_match(db: Session, match_id: UUID) -> Optional[Match]:
    committed_at = datetime.now()

    match = MatchRepository(db).find_by_id(match_id)
    match = Match(match_id, match.parties, match.created_at, committed_at, match.closed_at)
    MatchRepository(db).update(match)

    entry_links = MatchEntryLinkRepository(db).find_by_match_id(match_id)
    if not entry_links.entry_ids:
        MatchRepository(db).delete(match_id)
        return Match(match_id, [])
    
    entries = EntryRepository(db).find_by_query(EntryQuery(ids=entry_links.entry_ids))
    close_entries(db, entries, committed_at)

    return match

def make_match_with_new_entries(db: Session, entries: List[Entry]) -> Match:
    matching = Matching(entries)
    parties = parties_from_entries(matching.make_match())
    payload = Match(uuid4(), parties)
    return MatchRepository(db).save(payload)


def make_match_proto(db: Session, entries: List[Entry]) -> Match:
    matching = Matching(entries)
    parties = parties_from_entries(matching.make_match())
    payload = Match(uuid4(), parties)
    return ProtoMatchRepository(db).save(payload)


def parties_from_entries(entries: List[Entry]) -> List[Party]:
    return [Party(uuid4(), [Player(p.id, p.name, p.point) for p in e.players]) for e in entries]
