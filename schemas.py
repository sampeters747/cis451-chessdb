import inspect
from typing import List, Optional, Type

from fastapi import Form
from pydantic import BaseModel
from pydantic.fields import ModelField

# as_form function found here https://newbedev.com/fastapi-form-data-with-pydantic-model, required to
# use pydantic schema models to verify form input when normally they'd specify json input
# def as_form(cls: Type[BaseModel]):
#     new_parameters = []

#     for field_name, model_field in cls.__fields__.items():
#         model_field: ModelField  # type: ignore

#         if not model_field.required:
#             new_parameters.append(
#                 inspect.Parameter(
#                     model_field.alias,
#                     inspect.Parameter.POSITIONAL_ONLY,
#                     default=Form(model_field.default),
#                     annotation=model_field.outer_type_,
#                 )
#             )
#         else:
#             new_parameters.append(
#                 inspect.Parameter(
#                     model_field.alias,
#                     inspect.Parameter.POSITIONAL_ONLY,
#                     default=Form(...),
#                     annotation=model_field.outer_type_,
#                 )
#             )

#     async def as_form_func(**data):
#         return cls(**data)

#     sig = inspect.signature(as_form_func)
#     sig = sig.replace(parameters=new_parameters)
#     as_form_func.__signature__ = sig  # type: ignore
#     setattr(cls, 'as_form', as_form_func)
#     return cls

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


Player.update_forward_refs()
