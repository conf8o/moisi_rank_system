import domain.matching as domain
from sqlalchemy.orm import Session
from sqlalchemy import Column, ForeignKey, DateTime, String, Integer, Uuid
from sqlalchemy.dialects.postgresql import insert
from database import Base
from datetime import datetime
from collections import defaultdict
from typing import Optional


class Match(Base):
    id = Column("id", Uuid, primary_key=True)
    created_at = Column("created_at", DateTime, default=datetime.now, nullable=False)
    closed_at = Column("closed_at", DateTime)

    __tablename__ = "matches"


class Party(Base):
    id = Column("id", Uuid, primary_key=True)
    match_id = Column("match_id", Uuid, ForeignKey("matches.id", onupdate="CASCADE", ondelete="CASCADE"))

    __tablename__ = "parties"


class Entry(Base):
    id = Column("id", Uuid, primary_key=True)
    created_at = Column("created_at", DateTime, default=datetime.now, nullable=False)
    closed_at = Column("closed_at", DateTime)

    __tablename__ = "entries"


class Player(Base):
    id = Column("id", Uuid, primary_key=True)
    name = Column("name", String(255), nullable=False)
    point = Column("point", Integer, nullable=False)

    __tablename__ = "players"


class PartyPlayer(Base):
    party_id = Column("party_id", Uuid, ForeignKey("parties.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    player_id = Column("player_id", Uuid, ForeignKey("players.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)

    __tablename__ = "party_players"


class EntryPlayer(Base):
    entry_id = Column("entry_id", Uuid, ForeignKey("entries.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    player_id = Column("player_id", Uuid, ForeignKey("players.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)

    __tablename__ = "entry_players"


def _upsert_players(db: Session, players: list[Player]) -> None:
    insert_maps = [{"id": p.id, "name": p.name, "point": p.point} for p in players]
    players_insert = insert(Player).values(insert_maps)
    players_upsert = players_insert.on_conflict_do_update(
        index_elements=["id"],
        set_={
            "id": players_insert.excluded.id,
            "name": players_insert.excluded.name,
            "point": players_insert.excluded.point
        }
    )
    db.execute(players_upsert)


def _upsert_entry_players(db: Session, entry_players: list[EntryPlayer]) -> None:
    insert_maps = [{"player_id": e.player_id, "entry_id": e.entry_id} for e in entry_players]
    entry_players_insert = insert(EntryPlayer).values(insert_maps)
    entry_players_upsert = entry_players_insert.on_conflict_do_update(
        index_elements=["player_id"],
        set_={
            "player_id": entry_players_insert.excluded.player_id,
            "entry_id": entry_players_insert.excluded.entry_id
        }
    )
    db.execute(entry_players_upsert)


class EntryRepository(domain.AEntryRepository):
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def find_by_id(self, id: Uuid) -> Optional[domain.EntryEntity]:
        entry = self.db.query(Entry).filter(Entry.id==id).first()
        if not entry:
            return None
        
        players = self.db.query(Player) \
            .outerjoin(EntryPlayer, Player.id==EntryPlayer.player_id) \
            .filter(EntryPlayer.entry_id==id) \
            .all()
        players = [domain.Player(p.id, p.name, p.point) for p in players]
        domain_entry = domain.EntryEntity(entry.id, players, entry.closed_at)
        return domain_entry
    
    def find_by_query(self, query: domain.EntryQuery) -> list[domain.EntryEntity]:
        sql = self.db.query(Entry)
        if not query.is_closed:
            sql = sql.filter(Entry.closed_at==None)

        entries = sql.all()
        players = self.db.query(EntryPlayer.entry_id, Player) \
            .join(EntryPlayer, Player.id==EntryPlayer.player_id) \
            .filter(EntryPlayer.entry_id.in_(e.id for e in entries)) \
            .all()
        
        players_by_entry_id = defaultdict(list)
        for entry_id, player in players:
            players_by_entry_id[entry_id].append(domain.Player(player.id, player.name, player.point))
        
        domain_entries = []
        for e in entries:
            if query.has_players and not players_by_entry_id[e.id]:
                continue
            elif not query.has_players and players_by_entry_id[e.id]:
                continue
            else:
                domain_entry = domain.EntryEntity(e.id, players_by_entry_id[e.id], e.closed_at)
                domain_entries.append(domain_entry)
        return domain_entries

    def save(self, payload: domain.EntryEntity) -> domain.EntryEntity:
        entry_id = payload.id
        entry = self.db.query(Entry).filter(Entry.id==entry_id).first()
        if entry:
            entry.closed_at = payload.closed_at
            self.db.flush()
            return self.find_by_id(entry_id)
    
        entry = Entry()
        entry.id = entry_id
        
        self.db.add(entry)
        self.db.flush()

        players = []
        entry_players = []
        for domain_player in payload.players:
            player = Player()
            player.id = domain_player.id
            player.name = domain_player.name
            player.point = domain_player.point
            players.append(player)

            entry_player = EntryPlayer()
            entry_player.entry_id = entry.id
            entry_player.player_id = player.id
            entry_players.append(entry_player)


        _upsert_players(self.db, players)
        self.db.flush()

        _upsert_entry_players(self.db, entry_players)
        self.db.flush()

        return self.find_by_id(entry_id)


class MatchRepository(domain.AMatchRepository):
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def find_by_id(self, id: Uuid) -> Optional[domain.Match]:
        m = self.db.query(Match).filter(Match.id==id).first()
        if not m:
            return None
        
        parties = self.db.query(Party).filter(Party.match_id==id).all()
        players = self.db.query(PartyPlayer.party_id, Player) \
            .outerjoin(PartyPlayer, Player.id==PartyPlayer.player_id) \
            .filter(PartyPlayer.party_id.in_(p.id for p in parties)) \
            .all()
        
        players_by_party_id = defaultdict(list)
        for party_id, player in players:
            players_by_party_id[party_id].append(domain.Player(player.id, player.name, player.point))

        parties = [domain.Party(p.id, players_by_party_id[p.id]) for p in parties]
        return domain.Match(id, parties)

    def save(self, payload: domain.Match) -> domain.Match:
        match_id = payload.id

        domain_parties: list[domain.Party] = payload.parties

        match = Match()
        match.id = match_id
        self.db.add(match)
        self.db.flush()

        parties = []
        players = []
        party_players = []
        for domain_party in domain_parties:
            party = Party()
            party.id = domain_party.id
            party.match_id = match_id
            parties.append(party)

            domain_players = domain_party.players
            for domain_player in domain_players:
                player = Player()
                player.id = domain_player.id
                player.name = domain_player.name
                player.point = domain_player.point
                players.append(player)

                party_player = PartyPlayer()
                party_player.party_id = party.id
                party_player.player_id = player.id
                party_players.append(party_player)

        self.db.add_all(parties)
        _upsert_players(self.db, players)
        self.db.flush()

        self.db.add_all(party_players)
        self.db.flush()

        return self.find_by_id(match_id)
