from typing import Optional
from sqlalchemy.orm import Session
import models
import schemas

def get_player(db: Session, player_id: Optional[int]=None):
    if player_id:
        return db.query(models.Player).filter(models.Player.id == player_id).first()
    else:
        return db.query(models.Player).all()

def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = models.Player(birth_year=player.birth_year, first=player.first, last=player.last)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def delete_player(db: Session, player_id: int):
    db_player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if db_player:
        db.delete(db_player)
        db.commit()
        return True
    else:
        return False

def get_organization(db: Session, org_code: Optional[str]=None):
    if org_code:
        return db.query(models.Organization).filter(models.Organization.code == org_code).first()
    else:
        return db.query(models.Organization).all()

def create_organization(db: Session, organization: schemas.OrganizationCreate):
    db_org = models.Organization(code=organization.code, name=organization.name)
    try:
        db.add(db_org)
        db.commit()
        db.refresh(db_org)
        return db_org
    except:
        db.rollback()
        return None

def delete_organization(db: Session, org_code: str):
    db_org = db.query(models.Organization).filter(models.Organization.code == org_code).first()
    if db_org:
        db.delete(db_org)
        db.commit()
        return True
    else:
        return False

def get_rating(db: Session, player_id: Optional[int]=None, org_code: Optional[str]=None):
    if org_code and player_id:
        return db.query(models.Rating).filter(models.Rating.org_code == org_code and models.Rating.player_id == player_id).first()
    else:
        return db.query(models.Rating).all()


def create_rating(db: Session, rating: schemas.RatingCreate):
    db_rating = models.Rating(player_id=rating.player_id, org_code=rating.org_code, title=rating.title, rating_number=rating.rating_number)
    try:
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating
    except:
        db.rollback()
        print("Unable to create rating")
        return None