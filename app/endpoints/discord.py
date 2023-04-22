from fastapi import APIRouter, Depends, status
from typing import Dict, Any
from sqlalchemy.orm import Session
from database import get_db
import use_case.discord as discord
from uuid import UUID

router = APIRouter()

@router.post("/post_matching_result/{match_id}")
def post_matching_result(match_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    return discord.post_matching_result(db, UUID(match_id))
