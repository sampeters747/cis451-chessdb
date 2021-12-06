import inspect
from typing import List, Optional, Type

from fastapi import Form
from pydantic import BaseModel
from pydantic.fields import ModelField

class PlayerBase(BaseModel):
    birth_year: int
    first: str
    last: str

# @as_form
class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    ratings: List['Rating']

    class Config:
        orm_mode = True

class OrganizationBase(BaseModel):
    code: str
    name: str

# @as_form
class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    issued_ratings: List['Rating']

    class Config:
        orm_mode = True

class RatingBase(BaseModel):
    player_id: int
    org_code: str
    title: Optional[str] = None
    rating_number: int

# @as_form
class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    player: Player
    org: Organization

    class Config:
        orm_mode = True


class TournamentBase(BaseModel):
    org_code: str
    name: str
    year: int

# @as_form
class TournamentCreate(TournamentBase):
    pass

class Tournament(TournamentBase):
    id: int
    org: Organization

    class Config:
        orm_mode = True

class TournamentEntryBase(BaseModel):
    player_id: int
    tournament_id: int

class TournamentEntryCreate(TournamentEntryBase):
    pass

class TournamentEntry(TournamentEntryBase):
    player: Player
    tournament: Tournament

    class Config:
        orm_mode = True

Player.update_forward_refs()
