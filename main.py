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
    msg = None
    return templates.TemplateResponse("ratings.html", {"request": request, "ratings": db_ratings, "msg": msg})


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