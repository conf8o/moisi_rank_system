from fastapi import APIRouter, Depends, status
from typing import Dict, Any
from sqlalchemy.orm import Session
from database import get_db
from use_case import posting_matching_result
from uuid import UUID

router = APIRouter()

@router.post("/posting_matching_result/{match_id}")
def post_matching_result(match_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    return posting_matching_result.post_matching_result(db, UUID(match_id))
