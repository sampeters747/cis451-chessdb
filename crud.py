from typing import Optional, Text
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

def find_top_rating(db: Session, org_code: str):
    return db.query(models.Rating).filter(models.Rating.org_code == org_code).order_by(models.Rating.rating_number.desc()).first()

def create_tournament(db: Session, tournament: schemas.TournamentCreate):
    db_tournament = models.Tournament(org_code=tournament.org_code, name=tournament.name, year=tournament.year)
    try:
        db.add(db_tournament)
        db.commit()
        db.refresh(db_tournament)
        return db_tournament
    except:
        db.rollback()
        print("Unable to create tournament")
        return None

def get_tournament(db: Session, tournament_id: Optional[int]=None):
    if tournament_id:
        return db.query(models.Tournament).filter(models.Tournament.id == tournament_id).first()
    else:
        return db.query(models.Tournament).all()

def register_tournament_player(db: Session, entry: schemas.TournamentEntryCreate):
    db_entry = models.TournamentEntry(tournament_id=entry.tournament_id, player_id=entry.player_id)
    try:
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return db_entry
    except:
        db.rollback()
        print("Unable to register player")
        return None
