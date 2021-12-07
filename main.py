from os import name
from re import template
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm.session import Session
from starlette.requests import Request
import models
import schemas
import crud
from database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/summary", response_class=HTMLResponse)
async def summary_page(request: Request):
    return templates.TemplateResponse("summary.html", {"request": request})

@app.get("/logical", response_class=HTMLResponse)
async def logicaldesign_page(request: Request):
    return templates.TemplateResponse("logical.html", {"request": request})

@app.get("/physical", response_class=HTMLResponse)
async def physicaldesign_page(request: Request):
    return templates.TemplateResponse("physical.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/players", response_class=HTMLResponse)
async def players(request: Request, db: Session = Depends(get_db)):
    db_players = crud.get_player(db)
    return templates.TemplateResponse("players.html", {"request": request, "players": db_players})


@app.post("/players/delete", response_class=HTMLResponse)
async def delete_player(request: Request, db: Session = Depends(get_db), player_id: int = Form(...)):
    delete_succesful = crud.delete_player(db, player_id)
    if delete_succesful:
        msg = f"Successfully deleted player with ID {player_id}"
    else:
        msg = f"Attempted delete of player with ID {player_id} was unsuccessful. Are you sure that player exists?"
    db_players = crud.get_player(db)
    return templates.TemplateResponse("players.html", {"request": request,
                                                       "players": db_players,
                                                       "msg": msg})

@app.post("/players/create", response_class=HTMLResponse)
async def create_player(request: Request, db: Session = Depends(get_db), first: str = Form(...), last: str = Form(...), birth_year: int = Form(...)):
    player = schemas.PlayerCreate(
        birth_year=birth_year, first=first, last=last)
    db_player = crud.create_player(db, player)
    db_players = crud.get_player(db)
    msg = f"Successfully added player with ID {db_player.id}"
    return templates.TemplateResponse("players.html", {"request": request,
                                                       "players": db_players,
                                                       "msg": msg})


@app.get("/organizations", response_class=HTMLResponse)
async def organizations(request: Request, db: Session = Depends(get_db)):
    db_orgs = crud.get_organization(db)
    return templates.TemplateResponse("organizations.html", {"request": request, "organizations": db_orgs})


@app.post("/organizations/create", response_class=HTMLResponse)
async def create_org(request: Request, db: Session = Depends(get_db), code: str = Form(...), name: str = Form(...)):
    org = schemas.OrganizationCreate(code=code, name=name)
    db_org = crud.create_organization(db, org)
    db_orgs = crud.get_organization(db)
    if db_org:
        msg = f"Successfully added organization with code {org.code}"
    else:
        msg = f"Attempt to add organization with code {org.code} was unsuccessful. Is the organization code unique?"
    return templates.TemplateResponse("organizations.html", {"request": request,
                                                             "organizations": db_orgs,
                                                             "msg": msg})


@app.post("/organizations/delete", response_class=HTMLResponse)
async def delete_org(request: Request, db: Session = Depends(get_db), org_code: str = Form(...)):
    delete_succesful = crud.delete_organization(db, org_code)
    if delete_succesful:
        msg = f"Successfully deleted organization with org code {org_code}"
    else:
        msg = f"Attempted delete of organization with org code {org_code} was unsuccessful. Are you sure that organization exists?"
    db_orgs = crud.get_organization(db)
    return templates.TemplateResponse("organizations.html", {"request": request,
                                                             "organizations": db_orgs,
                                                             "msg": msg})


@app.get("/ratings", response_class=HTMLResponse)
async def ratings(request: Request, db: Session = Depends(get_db)):
    db_ratings = crud.get_rating(db)
    return templates.TemplateResponse("ratings.html", {"request": request, "ratings": db_ratings})


@app.post("/ratings/create", response_class=HTMLResponse)
async def create_rating(request: Request, db: Session = Depends(get_db), player_id: int = Form(...), org_code: str = Form(...), rating: int = Form(...), title: Optional[str] = Form(None)):
    rating_obj = schemas.RatingCreate(player_id=player_id, org_code=org_code, title=title, rating_number=rating)
    db_rating = crud.create_rating(db, rating_obj)
    if db_rating:
        msg = f"Successfully added rating of {db_rating.rating_number} to {db_rating.player.first+db_rating.player.first}"
    else:
        msg = f"Attempt to add rating of {rating_obj.rating_number} was unsuccessful. Do the player and organization exist?"
    db_ratings = crud.get_rating(db)
    return templates.TemplateResponse("ratings.html", {"request": request, "ratings": db_ratings, "msg": msg})

@app.post("/ratings/top", response_class=HTMLResponse)
async def find_top_rating(request: Request, db: Session = Depends(get_db), org_code: str = Form(...)):
    db_rating = crud.find_top_rating(db, org_code)
    if db_rating:
        msg = f"The top rated player in {db_rating.org.name} is {db_rating.player.first+db_rating.player.first} with a rating of {db_rating.rating_number}"
    else:
        msg = f"Attempt to find the top rated player in the organization {org_code} was unsuccessful. Are you sure the organization has issued any ratings?"
    db_ratings = crud.get_rating(db)
    return templates.TemplateResponse("ratings.html", {"request": request, "ratings": db_ratings, "msg": msg})

@app.get("/tournaments", response_class=HTMLResponse)
async def ratings(request: Request, db: Session = Depends(get_db)):
    db_tournaments = crud.get_tournament(db)
    return templates.TemplateResponse("tournaments.html", {"request": request, "tournaments": db_tournaments})

@app.post("/tournaments/create", response_class=HTMLResponse)
async def create_tournament(request: Request, db: Session = Depends(get_db), year: int = Form(...), org_code: str = Form(...), name: str = Form(...)):
    tournament_obj = schemas.TournamentCreate(org_code=org_code, name=name, year=year)
    db_tournament = crud.create_tournament(db, tournament_obj)
    if db_tournament:
        msg = f'Successfully created tournament named: "{db_tournament.name}" with ID:{db_tournament.id}. Add some players to the tournament using the second form!'
    else:
        msg = f"Attempt to create tournament was unsuccessful. Does the organization exist?"
    db_tournaments = crud.get_tournament(db)
    return templates.TemplateResponse("tournaments.html", {"request": request, "tournaments": db_tournaments, "msg": msg})

@app.post("/tournaments/register", response_class=HTMLResponse)
async def register_player(request: Request, db: Session = Depends(get_db), tournament_id: int = Form(...), player_id: int = Form(...)):
    entry_obj = schemas.TournamentEntryCreate(tournament_id=tournament_id, player_id=player_id)
    db_tournament_entry = crud.register_tournament_player(db, entry_obj)
    if db_tournament_entry:
        msg = f"Successfully registered {db_tournament_entry.player.first + ' '+ db_tournament_entry.player.last} in the tournament {db_tournament_entry.tournament.name}"
    else:
        msg = f"Player registration was unsuccessful. Are you sure the player ID and tournament ID  exist?"
    db_tournaments = crud.get_tournament(db)
    return templates.TemplateResponse("tournaments.html", {"request": request,
                                                             "tournaments": db_tournaments,
                                                             "msg": msg})