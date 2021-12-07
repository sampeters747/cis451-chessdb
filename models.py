from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Player(Base):
    __tablename__ = "players"
    # Columns
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    birth_year = Column(Integer)
    first = Column(String(18))
    last = Column(String(18))

    # Relationships
    # ratings variable provides easy access to relevant rows in Ratings table by checking what Rating.player_id foreign keys
    # reference the player object
    ratings = relationship("Rating", back_populates="player", cascade="all, delete, delete-orphan")
    tournaments = relationship("TournamentEntry", back_populates="player", cascade="all, delete, delete-orphan")
    white_games = relationship("Game", foreign_keys='Game.white_id', back_populates="white", cascade="all, delete, delete-orphan")
    black_games = relationship("Game", foreign_keys='Game.black_id', back_populates="black", cascade="all, delete, delete-orphan")
    sponsors = relationship("Sponsor", cascade="all, delete, delete-orphan", back_populates="player")

class Organization(Base):
    __tablename__ = "organizations"
    # Columns
    code = Column(String(10), primary_key=True, index=True)
    name = Column(String(48))

    # Relationships, provides easy access to relevant rows in Ratings table by checking what Rating.org_code foreign keys
    # reference the player object
    issued_ratings = relationship("Rating", back_populates="org", cascade="all, delete, delete-orphan")
    # More non-columns
    tournaments = relationship("Tournament", back_populates="org", cascade="all, delete, delete-orphan")

class Rating(Base):
    __tablename__ = "ratings"
    # Columns
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False, primary_key=True)
    org_code = Column(String(8), ForeignKey("organizations.code"), nullable=False, primary_key=True)
    title = Column(String(18), nullable=True)
    rating_number = Column(Integer)

    # Relationships
    # Relating player attribute in Rating class and ratings attribute in Player class, so when one is updated,
    # the other is automatically modified.
    player = relationship("Player", back_populates="ratings")
    org = relationship("Organization", back_populates="issued_ratings")

class Tournament(Base):
    __tablename__ = "tournaments"
    # Columns
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    org_code = Column(String(8), ForeignKey("organizations.code"), nullable=False)
    name = Column(String(36))
    year = Column(Integer)

    # Relationships
    org = relationship("Organization", back_populates="tournaments")
    players = relationship("TournamentEntry", back_populates="tournament")
    games = relationship("Game", back_populates="tournament")

class TournamentEntry(Base):
    __tablename__ = "tournamententry"
    # Columns
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False, primary_key=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=False, primary_key=True)

    # Relationships
    player = relationship("Player", back_populates="tournaments")
    tournament = relationship("Tournament", back_populates="players")

class Game(Base):
    __tablename__ = "games"
    # Columns
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    white_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    black_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=True)
    # 0 == black win, 1 == white win, 2 == draw
    result = Column(Integer, nullable=False)

    # Relationships
    white = relationship("Player", foreign_keys=[white_id], back_populates="white_games")
    black = relationship("Player", foreign_keys=[black_id], back_populates="black_games")
    tournament = relationship("Tournament", back_populates="games")
    moves = relationship("Move", back_populates="game")

class Move(Base):
    __tablename__ = "moves"
    # Columns
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False, primary_key=True)
    ply = Column(Integer, nullable=False, primary_key=True)
    # String representation of move using standard algebraic notation https://en.wikipedia.org/wiki/Algebraic_notation_(chess)
    move = Column(String(12), nullable=False)

    # Relationships
    game = relationship("Game", foreign_keys=[game_id], back_populates="moves")

class Sponsor(Base):
    __tablename__ = "sponsors"
    # Columns
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False, primary_key=True)
    company_name = Column(String(32), nullable=False, primary_key=True)
    amount = Column(Integer, nullable=False)

    # Relationships
    player = relationship("Player", foreign_keys=[player_id], back_populates="sponsors")
