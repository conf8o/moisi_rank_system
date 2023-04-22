from domain.matching import Match, MatchQuery, Player, Party
from infra.matching import MatchRepository
from uuid import UUID
from typing import Dict, Any
from external import discord
from sqlalchemy.orm import Session


def _player_to_json(player: Player) -> Dict[str, Any]:
    return {
        "id": player.id,
        "name": player.name,
        "point": player.point
    }


def _party_to_json(party: Party) -> Dict[str, Any]:
    return {
        "players": [_player_to_json(p) for p in party.players]
    }


def _match_to_json(match: Match) -> Dict[str, Any]:
    return {
        "id": match.id,
        "parties": [_party_to_json(p) for p in match.parties]
    }


def post_matching_result(db: Session, match_id: UUID) -> Dict[str, Any]:
    query = MatchQuery(id=match_id, is_committed=True)
    match = MatchRepository(db).find_by_query(query)

    if match:
        match_json = _match_to_json(match[0])
        res = discord.hook_v1_matching(match_json)
        return res
    else:
        return {"status_code": 404}