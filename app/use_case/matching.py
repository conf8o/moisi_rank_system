from domain.matching import AMatchRepository, Matching, Party, Entry, EntryEntity, Match, MatchQuery, Player, EntryQuery, MatchEntryLink, split_entries
from sqlalchemy.orm import Session
from infra.matching import MatchRepository, EntryRepository, MatchEntryLinkRepository, EntryPlayer
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

def delete_entry(db: Session, id: UUID) -> None:
    return EntryRepository(db).delete(id)

def cancel_entry(db: Session, player_id: UUID) -> None:
    return EntryRepository(db).delete_by_player_id(player_id)

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
    

def query_match(db: Session, **query) -> List[Match]:
    is_linked_entries = query.get("is_linked_entries")
    is_committed = query.get("is_committed")
    matches = MatchRepository(db).find_by_query(MatchQuery(is_committed))
    if is_linked_entries:
        new_matches = []
        for match in matches:
            entry_links = MatchEntryLinkRepository(db).find_by_match_id(match.id)
            if entry_links.entry_ids:
                new_matches.append(match)
        matches = new_matches
    return matches


def fetch_match(db: Session, match_id: UUID) -> Match:
    return MatchRepository(db).find_by_id(match_id)


def make_match(db: Session, entry_entities: List[EntryEntity]) -> List[Match]:
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

def make_match_with_new_entries(db: Session, entries: List[Entry]) -> List[Match]:
    entry_entities = [EntryEntity(uuid4(), e.players, None) for e in entries]
    for e in entry_entities:
        EntryRepository(db).save(e)
    return make_match(db, entry_entities)

def make_match_from_store(db: Session) -> List[Match]:
    empty_entry_query = EntryQuery(is_closed=False, has_players=False)
    empty_entries = EntryRepository(db).find_by_query(empty_entry_query)
    close_entries(db, empty_entries)

    entry_query = EntryQuery(is_closed=False, has_players=True)
    entry_entities = EntryRepository(db).find_by_query(entry_query)
    if not entry_entities:
        return []
    
    return make_match(db, entry_entities)

class MatchEntryEmptyError(Exception):
    pass

def commit_match(db: Session, match_id: UUID) -> Match:
    committed_at = datetime.now()

    match = MatchRepository(db).find_by_id(match_id)
    match = Match(match_id, match.parties, match.created_at, committed_at, match.closed_at)
    MatchRepository(db).update(match)

    entry_links = MatchEntryLinkRepository(db).find_by_match_id(match_id)
    if not entry_links.entry_ids:
        match.closed_at = datetime.now()
        MatchRepository(db).update(match)
        return Match(match_id, [])
    
    entries = EntryRepository(db).find_by_query(EntryQuery(ids=entry_links.entry_ids))
    close_entries(db, entries, committed_at)

    return match

def rollback_match(db: Session, match_id: UUID) -> Match:
    match = MatchRepository(db).find_by_query(MatchQuery(id=match_id, is_committed=True))
    if match:
        entry_links = MatchEntryLinkRepository(db).find_by_match_id(match_id)
        entries = EntryRepository(db).find_by_query(EntryQuery(ids=entry_links.entry_ids))
        for entry in entries:
            entry.closed_at = None
            update_entry(db, entries)

        match = match[0]
        match.closed_at = None
        MatchRepository(db).update(match_id)

    return fetch_match(db, match_id)


def make_match_proto(db: Session, entries: List[Entry]) -> Match:
    matching = Matching(entries)
    parties = parties_from_entries(matching.make_match())
    payload = Match(uuid4(), parties)
    return ProtoMatchRepository(db).save(payload)


def parties_from_entries(entries: List[Entry]) -> List[Party]:
    return [Party(uuid4(), [Player(p.id, p.name, p.point) for p in e.players]) for e in entries]
