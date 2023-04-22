from typing import Optional, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from use_case import matching
from domain import matching as domain
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, timezone
from typing import List
from zoneinfo import ZoneInfo

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
    players: List[Player]

    def to_model(self) -> domain.Entry:
        return domain.Entry([p.to_model() for p in self.players])
    
    @staticmethod
    def from_model(entry: domain.Entry) -> 'Entry':
        return Entry(players=[Player.from_model(p) for p in entry.players])


class EntryEntity(BaseModel):
    id: Optional[str]
    players: List[Player]
    closed_at: Optional[datetime]

    def to_model(self) -> domain.EntryEntity:
        if self.closed_at:
            closed_at = self.closed_at.astimezone(timezone.utc)
        else:
            closed_at = None

        return domain.EntryEntity(UUID(self.id), [p.to_model() for p in self.players], closed_at)
    
    @staticmethod
    def from_model(entry: domain.EntryEntity) -> 'EntryEntity':
        if entry.closed_at:
            closed_at = entry.closed_at.astimezone(timezone.utc)
        else:
            closed_at = None

        return EntryEntity(id=str(entry.id), players=[Player.from_model(p) for p in entry.players], closed_at=closed_at)


class Party(BaseModel):
    players: List[Player]

    @staticmethod
    def from_model(party: domain.Party) -> 'Party':
        return Party(players=[Player.from_model(p) for p in party.players])


class EntryQueryRequest(BaseModel):
    is_closed: bool = False
    has_players: bool = True

    def to_model(self) -> domain.EntryQuery:

        return domain.EntryQuery(is_closed=self.is_closed, has_players=self.has_players)

class MatchMakingRequest(BaseModel):
    entries: List[Entry]

    def to_model(self) -> List[domain.Entry]:
        return [e.to_model() for e in self.entries]


class Match(BaseModel):
    id: str
    parties: List[Party]
    created_at: Optional[datetime]
    committed_at: Optional[datetime]
    closed_at: Optional[datetime]

    @staticmethod
    def from_model(match: domain.Match) -> 'Match':
        if match.committed_at:
            committed_at = match.committed_at.astimezone(ZoneInfo("Asia/Tokyo"))
        else:
            committed_at = None

        if match.closed_at:
            closed_at = match.closed_at.astimezone(ZoneInfo("Asia/Tokyo"))
        else:
            closed_at = None
            
        if match.created_at:
            created_at = match.created_at.astimezone(ZoneInfo("Asia/Tokyo"))
        else:
            created_at = None

        return Match(
            id=str(match.id),
            parties=[Party.from_model(p) for p in match.parties],
            created_at=created_at,
            committed_at=committed_at,
            closed_at=closed_at
        )


class MatchMakingResponse(BaseModel):
    matches: List[Match]

    @staticmethod
    def from_model(matches: List[domain.Match]) -> 'MatchMakingResponse':
        return MatchMakingResponse(matches=[Match.from_model(m) for m in matches])


@router.get("/")
def index():
    return "matching"


@router.post("/entries", response_model=Entry, status_code=status.HTTP_201_CREATED)
def create_entry(req: Entry, db: Session = Depends(get_db)) -> EntryEntity:
    entry: domain.EntryEntity = matching.create_entry(db, req.to_model())
    return EntryEntity.from_model(entry)


@router.get("/entries")
def query_entry(is_closed: bool = False, has_players: bool = True, db: Session = Depends(get_db)) -> List[EntryEntity]:
    entries = matching.query_entry(db, domain.EntryQuery(is_closed=is_closed, has_players=has_players))
    return [EntryEntity.from_model(e) for e in entries]


@router.put("/entries/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_entry(id: str, entry: EntryEntity, db: Session = Depends(get_db)) -> None:
    e = entry.to_model()
    e.id = UUID(id)
    matching.update_entry(db, e)
    return 

@router.delete("/entries/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(id: str, db: Session = Depends(get_db)) -> None:
    matching.delete_entry(db, UUID(id))
    return

@router.delete("/players/{id}/entry", status_code=status.HTTP_204_NO_CONTENT)
def cancel_entry(player_id: str, db: Session = Depends(get_db)) -> None:
    matching.cancel_entry(db, UUID(player_id))
    return

@router.get("/matches", response_model=List[Match])
def query_matching(is_linked_entries: bool=False, db: Session = Depends(get_db)) -> List[Match]:
    return [Match.from_model(m) for m in matching.query_match(db, is_linked_entries=is_linked_entries)]


@router.get("/matches/{id}", response_model=Match)
def fetch_matching(id: str, db: Session = Depends(get_db)) -> Match:
    return Match.from_model(matching.fetch_match(db, UUID(id)))


@router.post("/match_making", response_model=MatchMakingResponse, status_code=status.HTTP_201_CREATED)
def make_match_from_store(db: Session = Depends(get_db)):
    m: List[domain.Match] = matching.make_match_from_store(db)
    return MatchMakingResponse.from_model(m)


@router.post("/match_committing/{id}", response_model=Match)
def commit_match(id: str, db: Session = Depends(get_db)) -> Match:
    m: domain.Match = matching.commit_match(db, UUID(id))
    return Match.from_model(m)

@router.post("/match_rollbacking/{id}")
def rollback_match(id: str, db: Session = Depends(get_db)) -> None:
    matching.rollback_match(db, UUID(id))
    return

@router.post("/match_making_with_new_entries", response_model=MatchMakingResponse, status_code=status.HTTP_201_CREATED)
def make_match_with_new_entries(req: MatchMakingRequest, db: Session = Depends(get_db)):
    m: List[domain.Match] = matching.make_match_with_new_entries(db, req.to_model())
    return MatchMakingResponse.from_model(m)


@router.post("/match_making_proto", response_model=MatchMakingResponse, status_code=status.HTTP_200_OK)
def make_match_proto(req: MatchMakingRequest, db: Session = Depends(get_db)) -> MatchMakingResponse:
    m: List[domain.Match] = matching.make_match_with_new_entries(db, req.to_model())
    return MatchMakingResponse.from_model(m)
