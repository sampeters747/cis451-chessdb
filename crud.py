from typing import Optional
from sqlalchemy.orm import Session
import models
import schemas


def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = models.Player(birth_year=player.birth_year, first=player.first, last=player.last)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def get_player(db: Session, player_id: Optional[int]=None):
    if player_id:
        return db.query(models.Player).filter(models.Player.id == player_id).first()
    else:
        return db.query(models.Player).all()

def delete_player(db: Session, player_id: int):
    db_player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if db_player:
        db.delete(db_player)
        db.commit()
        return True
    else:
        return False