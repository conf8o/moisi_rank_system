from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from use_case import matching
from domain import matching as domain
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

router = APIRouter()


class Player(BaseModel):
    id: str
    name: str
    point: int
    
    def to_model(self) -> domain.Player:
        return domain.Player(UUID(self.id), self.name, self.point)
    
    @staticmethod
    def from_model(player: domain.Player) -> 'Player':
        return Player(id=str(player.id), name=player.name, point=player.point)


class Entry(BaseModel):
    players: list[Player]

    def to_model(self) -> domain.Entry:
        return domain.Entry([p.to_model() for p in self.players])
    
    @staticmethod
    def from_model(entry: domain.Entry) -> 'Entry':
        return Entry(players=[Player.from_model(p) for p in entry.players])


class EntryEntity(BaseModel):
    id: Optional[str]
    players: list[Player]
    closed_at: Optional[datetime]

    def to_model(self) -> domain.EntryEntity:
        return domain.EntryEntity(self.id, [p.to_model() for p in self.players], self.closed_at)
    
    @staticmethod
    def from_model(entry: domain.EntryEntity) -> 'EntryEntity':
        return EntryEntity(id=str(entry.id), players=[Player.from_model(p) for p in entry.players], closed_at=entry.closed_at)


class Party(BaseModel):
    players: list[Player]

    @staticmethod
    def from_model(party: domain.Party) -> 'Party':
        return Party(players=[Player.from_model(p) for p in party.players])


class EntryQueryRequest(BaseModel):
    is_closed: bool = False
    has_players: bool = True

    def to_model(self) -> domain.EntryQuery:
        return domain.EntryQuery(is_closed=self.is_closed, has_players=self.has_players)

class MatchMakingRequest(BaseModel):
    entries: list[Entry]

    def to_model(self) -> list[domain.Entry]:
        return [e.to_model() for e in self.entries]


class MatchMakingResponse(BaseModel):
    parties: list[Party]

    @staticmethod
    def from_model(parties: list[domain.Party]) -> 'MatchMakingResponse':
        return MatchMakingResponse(parties=[Party.from_model(p) for p in parties])


@router.get("/")
def index():
    return "matching"


@router.post("/entries", response_model=Entry)
def create_entry(req: Entry, db: Session = Depends(get_db)) -> Entry:
    entry: domain.EntryEntity = matching.create_entry(db, req.to_model())
    return EntryEntity.from_model(entry)


@router.get("/entries")
def query_entry(is_closed: bool = False, has_players: bool = True, db: Session = Depends(get_db)) -> list[Entry]:
    entries = matching.query_entry(db, domain.EntryQuery(is_closed=is_closed, has_players=has_players))
    return [EntryEntity.from_model(e) for e in entries]

@router.put("/entries/{id}")
def update_entry(id: str, entry: EntryEntity, db: Session = Depends(get_db)) -> None:
    e = entry.to_model()
    e.id = UUID(id)
    matching.update_entry(db, e)
    return 

@router.get("/matching")
def query_matching(db: Session = Depends(get_db)):
    return ""


@router.post("/match_making", response_model=MatchMakingResponse)
def make_match(db: Session = Depends(get_db)):
    m: domain.Match = matching.make_match(db)
    return MatchMakingResponse.from_model(m.parties)


@router.post("/match_making_with_new_entries", response_model=MatchMakingResponse)
def make_match_with_new_entries(req: MatchMakingRequest, db: Session = Depends(get_db)):
    m: domain.Match = matching.make_match_with_new_entries(db, req.to_model())
    return MatchMakingResponse.from_model(m.parties)


@router.post("/match_making_proto", response_model=MatchMakingResponse)
def make_match_proto(req: MatchMakingRequest, db: Session = Depends(get_db)) -> MatchMakingResponse:
    m: domain.Match = matching.make_match_with_new_entries(db, req.to_model())
    return MatchMakingResponse.from_model(m.parties)
