from re import template
from typing import List

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
# templates.env.globals['base_url'] = "www.google.com"


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", { "request" : request})

@app.get("/players", response_class=HTMLResponse)
async def players(request: Request, db: Session = Depends(get_db)):
    db_players = crud.get_player(db)
    return templates.TemplateResponse("players.html", { "request" : request, "players": db_players})

@app.post("/players/delete", response_class=HTMLResponse)
async def delete_player(request: Request, db: Session = Depends(get_db), player_id: int=Form(...)):
    delete_succesful = crud.delete_player(db, player_id)
    if delete_succesful:
        msg = f"Successfully deleted player with ID {player_id}"
    else:
        msg = f"Attempted delete of player with ID {player_id} was unsuccessful. Are you sure that player exists?"
    db_players = crud.get_player(db)
    return templates.TemplateResponse("players.html", { "request" : request,
                                                         "players": db_players,
                                                         "msg": msg})

@app.post("/players/create", response_class=HTMLResponse)
async def create_player(request: Request, db: Session = Depends(get_db), first: str=Form(...), last: str=Form(...), birth_year: int=Form(...)):
    player = {
        'first': first,
        'last': last,
        'birth_year': birth_year
    }
    db_players = crud.get_player(db)
    return templates.TemplateResponse("players.html", { "request" : request,
                                                         "players": db_players,
                                                         "msg": msg})

# @app.post("/players", response_class=HTMLResponse)
# async def players(request: Request, player: schemas.PlayerCreate = Depends(schemas.PlayerCreate.as_form), db: Session = Depends(get_db)):
#     db_player = crud.create_player(db, player)
#     return templates.TemplateResponse("players.html", { "request" : request})


# @app.post("/player/", response_model=schemas.Player)
# async def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
#     return crud.create_player(db, player)

# @app.post("/player/", response_model=schemas.Player)
# async def create_player(player: schemas.PlayerCreate = Depends(schemas.PlayerCreate.as_form), db: Session = Depends(get_db)):
#     return crud.create_player(db, player)

# @app.get("/player/", response_model=List[schemas.Player])
# async def read_players(db: Session = Depends(get_db)):
#     return crud.get_player(db)

# @app.get("/player/{player_id}", response_model=schemas.Player)
# async def read_players(player_id: int, db: Session = Depends(get_db)):
#     return crud.get_player(db, player_id=player_id)
